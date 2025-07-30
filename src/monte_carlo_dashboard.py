#!/usr/bin/env python3
"""
Monte Carlo Data Observability Dashboard - Complete Learning Platform
=====================================================================

This comprehensive dashboard demonstrates enterprise-level data observability concepts
inspired by Monte Carlo's platform. Perfect for learning and showcasing data engineering skills.

Key Features:
- Real-time data quality monitoring with multi-dimensional scoring
- AI-powered analysis using OpenAI integration 
- Live file system monitoring with automatic ingestion
- Monte Carlo SDK integration patterns (demo and production modes)
- Professional deployment automation and error handling

Architecture Components:
- DataManager: Handles DuckDB operations and CSV file ingestion
- AIAnalyzer: Provides OpenAI-powered data quality insights
- LiveMonitor: Real-time file system monitoring with watchdog
- MonteCarloIntegration: SDK client for enterprise observability patterns

Learning Objectives:
- Understanding data quality metrics and scoring algorithms
- Enterprise SDK integration patterns and authentication
- Real-time monitoring system architecture
- Production-ready error handling and logging practices
"""

import os
import time
import pandas as pd
import duckdb
import streamlit as st
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from dotenv import load_dotenv
import threading
import sys

# Try to import Monte Carlo SDK from pycarlo_integration
try:
    sys.path.append(str(Path(__file__).parent.parent / "pycarlo_integration"))
    from monte_carlo_client import MonteCarloIntegration
    MONTE_CARLO_SDK_AVAILABLE = True
except ImportError:
    MONTE_CARLO_SDK_AVAILABLE = False

# ==========================================
# CONFIGURATION MANAGEMENT
# ==========================================

class Config:
    """
    Centralized Configuration Management
    ===================================
    
    Handles environment variable loading and provides secure access to configuration.
    Supports both .env files and system environment variables.
    
    Key Features:
    - Automatic .env file discovery from project root
    - Secure API key management for OpenAI and Monte Carlo
    - Database path configuration for DuckDB
    - Logging level configuration
    
    Usage Example:
        config = Config()
        api_key = config.openai_api_key  # Raises error if missing
        db_path = config.duckdb_path     # Returns default if not set
    """
    
    def __init__(self, env_file: Optional[str] = None):
        if env_file:
            load_dotenv(env_file)
        else:
            # Look for .env file in project root (parent of src directory)
            project_root = Path(__file__).parent.parent
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
            else:
                # Fallback: try current directory
                load_dotenv()
    
    @property
    def openai_api_key(self) -> str:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return key
    
    @property
    def openai_organization(self) -> str:
        return os.getenv("OPENAI_ORGANIZATION", "")
    
    @property
    def openai_project(self) -> str:
        return os.getenv("OPENAI_PROJECT", "")
    
    @property
    def duckdb_path(self) -> str:
        return os.getenv("DUCKDB_PATH", "database/monte-carlo.duckdb")
    
    @property
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")

# Global configuration
config = Config()

# ==========================================
# DATA MANAGEMENT
# ==========================================

class DataManager:
    """
    Database Operations and Data Loading Manager
    ===========================================
    
    Handles all DuckDB operations, CSV file ingestion, and live statistics calculation.
    Implements enterprise patterns for data quality monitoring and validation.
    
    Key Features:
    - Bulk CSV file loading with automatic table creation
    - Real-time file ingestion with data validation
    - Multi-dimensional quality scoring (completeness, consistency, timeliness)
    - Live statistics calculation for dashboard metrics
    
    Quality Scoring Algorithm:
    - Completeness: Percentage of non-null description fields
    - Content Quality: Penalizes descriptions shorter than 10 characters
    - Overall Score: (Valid Records / Total Records) × 100
    
    Usage Example:
        data_manager = DataManager("database/analytics.duckdb")
        data_manager.load_csv_files("sample_data/")
        stats = data_manager.get_live_stats()
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def get_connection(self):
        """Get database connection."""
        return duckdb.connect(self.db_path)
    
    def load_csv_files(self, data_dir: str = "data") -> None:
        """Load all CSV files from directory into DuckDB."""
        con = self.get_connection()
        data_path = Path(data_dir)
        csv_files = list(data_path.glob("*.csv"))
        
        print(f"📁 Found {len(csv_files)} CSV files in {data_dir} directory")
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                table_name = csv_file.stem
                
                print(f"📊 Loading {csv_file.name} -> {table_name} table ({len(df)} rows)")
                
                # Create table with description_length column for quality checks
                con.execute(f"DROP TABLE IF EXISTS {table_name}")
                con.register(f"{table_name}_df", df)
                
                if table_name == "product_operations_incidents_2025":
                    # Create enhanced table with calculated fields
                    con.execute(f"""
                        CREATE TABLE {table_name} AS 
                        SELECT *, LENGTH(description) as description_length 
                        FROM {table_name}_df
                    """)
                    
                    # Create summarize_model view/table
                    con.execute("""
                        CREATE OR REPLACE TABLE summarize_model AS
                        SELECT 
                            id,
                            title,
                            description,
                            description_length
                        FROM product_operations_incidents_2025
                    """)
                else:
                    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}_df")
                
            except Exception as e:
                print(f"❌ Error loading {csv_file}: {e}")
        
        con.close()
    
    def ingest_csv_file(self, file_path: str) -> None:
        """Ingest a single CSV file into the database."""
        try:
            df = pd.read_csv(file_path)
            con = self.get_connection()
            
            # Determine table name
            file_name = Path(file_path).stem
            
            # For demo files, append to existing tables
            if "product_operations" in file_name.lower() or "demo" in file_name.lower():
                # Get current max ID
                try:
                    max_id = con.execute("SELECT MAX(id) FROM product_operations_incidents_2025").fetchone()[0] or 0
                except:
                    max_id = 0
                
                # Add new IDs
                df['id'] = range(max_id + 1, max_id + len(df) + 1)
                df['description_length'] = df['description'].str.len()
                
                # Insert new data
                con.register("new_data", df)
                con.execute("INSERT INTO product_operations_incidents_2025 SELECT * FROM new_data")
                con.execute("""
                    INSERT INTO summarize_model 
                    SELECT id, title, description, description_length 
                    FROM new_data
                """)
                
                print(f"✅ Added {len(df)} new records to product_operations_incidents_2025 table")
            
            con.close()
            
        except Exception as e:
            print(f"❌ Error ingesting {file_path}: {e}")
    
    def get_live_stats(self) -> Dict:
        """
        Calculate Real-time Data Quality Statistics
        ==========================================
        
        Implements Monte Carlo-style quality scoring with multiple dimensions:
        
        Quality Metrics:
        - Total Records: Overall data volume
        - Recent Records: New data growth (last 10 records)
        - NULL Descriptions: Completeness validation
        - Short Descriptions: Content quality validation (<10 chars)
        - Quality Score: Composite score = (Valid Records / Total) × 100
        
        Returns:
            Dict containing all quality metrics for dashboard display
            
        Algorithm Details:
        1. Count total records in summarize_model table
        2. Identify recent additions (last 10 IDs)
        3. Detect NULL or empty description fields
        4. Flag short content (< 10 characters)
        5. Calculate composite quality score
        
        This mirrors enterprise data observability patterns used by Monte Carlo.
        """
        try:
            con = self.get_connection()
            
            total_records = con.execute("SELECT COUNT(*) FROM summarize_model").fetchone()[0]
            recent_records = con.execute("""
                SELECT COUNT(*) FROM summarize_model 
                WHERE id > (SELECT MAX(id) - 10 FROM summarize_model)
            """).fetchone()[0]
            
            null_descriptions = con.execute("""
                SELECT COUNT(*) FROM summarize_model 
                WHERE description IS NULL OR description = ''
            """).fetchone()[0]
            
            short_descriptions = con.execute("""
                SELECT COUNT(*) FROM summarize_model 
                WHERE description_length < 10 AND description IS NOT NULL
            """).fetchone()[0]
            
            # Calculate Multi-dimensional Quality Score
            # This algorithm demonstrates enterprise data quality patterns:
            # 1. Completeness: Percentage of records with valid descriptions
            # 2. Content Quality: Penalize short or empty content
            # 3. Weighted Scoring: Both NULL and short content reduce overall score
            quality_score = ((total_records - null_descriptions - short_descriptions) / total_records * 100) if total_records > 0 else 0
            
            con.close()
            
            return {
                'total_records': total_records,
                'recent_records': recent_records,
                'null_descriptions': null_descriptions,
                'short_descriptions': short_descriptions,
                'quality_score': quality_score
            }
        except Exception as e:
            st.error(f"Error getting stats: {e}")
            return {}

# ==========================================
# AI ANALYSIS
# ==========================================

class AIAnalyzer:
    """
    AI-Powered Data Quality Analysis
    ===============================
    
    Integrates OpenAI GPT models to provide intelligent data quality insights.
    Demonstrates enterprise AI integration patterns for observability platforms.
    
    Key Features:
    - Natural language data quality assessments
    - Automated anomaly detection and explanation
    - Business impact analysis of quality issues
    - Pattern recognition in data quality trends
    
    AI Analysis Pipeline:
    1. Content summarization with quality context
    2. Automated issue classification (OK/WARNING/ERROR)
    3. Actionable recommendations for data quality improvement
    4. Graceful degradation when AI services unavailable
    
    This showcases how modern data platforms integrate AI for enhanced observability.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        self._setup_client()
        
    def _setup_client(self):
        """Initialize OpenAI client."""
        try:
            self.client = OpenAI(
                organization=self.config.openai_organization,
                project=self.config.openai_project,
                api_key=self.config.openai_api_key
            )
        except Exception as e:
            print(f"Warning: OpenAI client setup failed: {e}")
    
    def generate_summary(self, text: str) -> str:
        """Generate AI summary with quality assessment."""
        if not self.client:
            return "AI analysis unavailable (no OpenAI configuration)"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """You are a data quality analyst that summarizes content and identifies potential issues. 
                    After your summary, add a DATA QUALITY section that flags any concerns like:
                    - Very short content (less than 10 words)
                    - Suspicious patterns or anomalies
                    - Missing context or incomplete information
                    - Potential data corruption indicators
                    Format: SUMMARY: [your summary] | DATA QUALITY: [OK/WARNING/ERROR] - [reason if not OK]"""},
                    {"role": "user", "content": f"Analyze this data for summary and quality issues:\n\n{text}"}
                ],
                temperature=0.3,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e} | DATA QUALITY: ERROR - API failure"
    
    def analyze_all_data(self, data_manager: DataManager) -> Tuple[List, List]:
        """Analyze all data and return summaries and alerts."""
        con = data_manager.get_connection()
        rows = con.execute("SELECT id, title, description FROM summarize_model").fetchall()
        con.close()
        
        summaries = []
        ai_alerts = []
        
        for row_id, title, description in rows:
            result = self.generate_summary(description)
            
            # Parse quality indicators
            if " | DATA QUALITY: " in result:
                summary_part, quality_part = result.split(" | DATA QUALITY: ", 1)
                
                reason = None
                if quality_part.startswith("ERROR"):
                    reason = quality_part
                elif quality_part.startswith("WARNING"):
                    reason = quality_part
                
                summaries.append((row_id, title, description, summary_part, reason))
                if reason:
                    ai_alerts.append((row_id, title, reason))
            else:
                summaries.append((row_id, title, description, result, None))
        
        return summaries, ai_alerts

# ==========================================
# LIVE MONITORING
# ==========================================

class LiveMonitor:
    """
    Real-time File System Monitoring
    ===============================
    
    Implements enterprise-grade file monitoring using the Watchdog library.
    Automatically detects and processes new CSV files for immediate quality assessment.
    
    Architecture:
    - Observer Pattern: Watchdog Observer monitors file system events
    - Event Handler: CSVFileHandler processes new CSV files automatically
    - Background Processing: Non-blocking file monitoring with threading
    - Automatic Integration: New files immediately appear in dashboard
    
    This demonstrates real-time data ingestion patterns used in production
    data observability platforms like Monte Carlo.
    """
    
    def __init__(self, data_manager: DataManager, watch_dir: str = "sample_data"):
        self.data_manager = data_manager
        self.watch_dir = watch_dir
        self.observer = None
        
    def start_monitoring(self):
        """Start file monitoring in background."""
        if self.observer and self.observer.is_alive():
            return
            
        handler = CSVFileHandler(self.data_manager)
        self.observer = Observer()
        self.observer.schedule(handler, self.watch_dir, recursive=False)
        self.observer.start()
        print(f"🔍 Started monitoring {self.watch_dir}/ for new CSV files...")
    
    def stop_monitoring(self):
        """Stop file monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()

class CSVFileHandler(FileSystemEventHandler):
    """
    CSV File Event Handler
    =====================
    
    Processes file system events specifically for CSV files.
    Implements immediate data ingestion upon file creation.
    
    Event Processing:
    1. Detects new CSV file creation events
    2. Waits for file write completion (1 second buffer)
    3. Triggers automatic data ingestion via DataManager
    4. Provides real-time feedback to console and dashboard
    
    This pattern enables real-time data pipeline automation.
    """
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            print(f"\n🔥 NEW CSV DETECTED: {event.src_path}")
            time.sleep(1)  # Let file finish writing
            self.data_manager.ingest_csv_file(event.src_path)
            print("✅ File ingested! Dashboard will update automatically.")

# ==========================================
# STREAMLIT DASHBOARD
# ==========================================

def setup_dashboard():
    """Configure Streamlit dashboard."""
    st.set_page_config(
        page_title="Monte Carlo Data Observability",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Monte Carlo Data Observability Demo")
    st.caption(f"All-in-One Dashboard | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def show_live_monitoring(data_manager: DataManager, live_monitor: LiveMonitor, ai_analyzer: AIAnalyzer):
    """Display live monitoring tab."""
    st.subheader("🔴 Live Demo Monitor")
    
    # Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        auto_refresh = st.checkbox("🔄 Auto-refresh (10 seconds)", value=False)
    
    with col2:
        if st.button("📊 Refresh Now"):
            st.rerun()
    
        with col3:
            if st.button("🎬 Start Monitor"):
                live_monitor.start_monitoring()
                st.success("Monitor started! Drop CSV files in sample_data/ folder")    # Live statistics
    stats = data_manager.get_live_stats()
    if stats:
        metric_cols = st.columns(5)
        
        with metric_cols[0]:
            st.metric("📊 Total Records", stats['total_records'], stats['recent_records'])
        with metric_cols[1]:
            st.metric("✅ Quality Score", f"{stats['quality_score']:.1f}%")
        with metric_cols[2]:
            st.metric("🚨 NULL Values", stats['null_descriptions'])
        with metric_cols[3]:
            st.metric("⚠️ Short Content", stats['short_descriptions'])
        with metric_cols[4]:
            st.metric("🕐 Last Update", datetime.now().strftime("%H:%M:%S"))
    
    # Recent records with enhanced description analysis
    st.subheader("📋 Recent Records & Description Quality")
    
    # Description analysis options
    col1, col2 = st.columns([3, 1])
    with col1:
        show_descriptions = st.checkbox("📝 Show Full Descriptions", value=False)
    with col2:
        analyze_live = st.checkbox("🤖 Live AI Analysis", value=False)
    
    try:
        con = data_manager.get_connection()
        recent_data = con.execute("""
            SELECT id, title, description, description_length
            FROM summarize_model 
            ORDER BY id DESC 
            LIMIT 10
        """).fetchdf()
        
        if not recent_data.empty:
            # Enhanced quality analysis
            recent_data['Quality Status'] = recent_data.apply(lambda row: 
                "🚨 NULL" if pd.isna(row['description']) or row['description'] == '' 
                else "⚠️ SHORT" if row['description_length'] < 10 
                else "⚠️ LONG" if row['description_length'] > 200
                else "✅ GOOD", axis=1)
            
            # Description quality scoring
            recent_data['Quality Score'] = recent_data.apply(lambda row:
                0 if pd.isna(row['description']) or row['description'] == ''
                else 30 if row['description_length'] < 10
                else 70 if row['description_length'] < 50
                else 90 if row['description_length'] < 200
                else 85, axis=1)
            
            # Prepare display columns
            display_cols = ['id', 'title', 'Quality Status', 'Quality Score', 'description_length']
            if show_descriptions:
                display_cols.append('description')
            
            # Live AI analysis if enabled
            if analyze_live and ai_analyzer and ai_analyzer.client:
                st.info("🤖 Running live AI analysis on recent records...")
                recent_data['AI Insight'] = recent_data['description'].apply(
                    lambda desc: ai_analyzer.generate_summary(str(desc))[:100] + "..." 
                    if pd.notna(desc) and desc != '' else "No content to analyze"
                )
                display_cols.append('AI Insight')
            
            st.dataframe(recent_data[display_cols], use_container_width=True)
            
            # Description quality distribution
            if len(recent_data) > 0:
                st.subheader("📊 Description Quality Distribution")
                quality_counts = recent_data['Quality Status'].value_counts()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    good_count = quality_counts.get('✅ GOOD', 0)
                    st.metric("✅ Good Quality", good_count, f"{good_count/len(recent_data)*100:.1f}%")
                with col2:
                    short_count = quality_counts.get('⚠️ SHORT', 0)
                    st.metric("⚠️ Short Descriptions", short_count, f"{short_count/len(recent_data)*100:.1f}%")
                with col3:
                    null_count = quality_counts.get('🚨 NULL', 0)
                    st.metric("🚨 NULL Descriptions", null_count, f"{null_count/len(recent_data)*100:.1f}%")
        else:
            st.info("No records found")
        
        con.close()
    except Exception as e:
        st.error(f"Error loading data: {e}")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()

def show_ai_analysis(data_manager: DataManager, ai_analyzer: AIAnalyzer):
    """Display AI analysis tab."""
    st.subheader("🤖 AI-Powered Data Analysis")
    
    if st.button("🔍 Run AI Analysis"):
        with st.spinner("Analyzing data with AI..."):
            summaries, ai_alerts = ai_analyzer.analyze_all_data(data_manager)
            
            # Display alerts
            if ai_alerts:
                st.subheader("🚨 AI Quality Alerts")
                for row_id, title, reason in ai_alerts:
                    st.error(f"Row {row_id} - {title}: {reason}")
            else:
                st.success("✅ No AI quality issues detected!")
            
            # Display summaries
            st.subheader("📋 AI Analysis Results")
            if summaries:
                df = pd.DataFrame(summaries, columns=['ID', 'Title', 'Description', 'AI Summary', 'Issue'])
                df['Issue'] = df['Issue'].fillna('✅ OK')
                st.dataframe(df[['ID', 'Title', 'AI Summary', 'Issue']], use_container_width=True)

def render_monte_carlo_sdk_tab():
    """Render the comprehensive Monte Carlo SDK integration tab"""
    st.header("🔗 Monte Carlo SDK Integration")
    st.markdown("*Complete demonstration of production-ready pycarlo SDK capabilities*")
    
    try:
        # Initialize Monte Carlo client
        client = MonteCarloIntegration(demo_mode=True)
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏠 Overview", 
            "📊 Quality Metrics", 
            "🚨 Incident Management", 
            "⚙️ Rule Management",
            "🔌 API Patterns"
        ])
        
        with tab1:
            render_sdk_overview(client)
        
        with tab2:
            render_quality_metrics_section(client)
        
        with tab3:
            render_incident_management_section(client)
        
        with tab4:
            render_rule_management_section(client)
        
        with tab5:
            render_api_patterns_section(client)
    
    except Exception as e:
        st.error(f"Error loading Monte Carlo SDK: {e}")
        st.info("💡 Ensure Monte Carlo SDK is properly configured")
        st.code("""
# To enable production mode:
export MONTE_CARLO_API_ID="your-api-id"
export MONTE_CARLO_API_TOKEN="your-api-token"
export MONTE_CARLO_DEMO_MODE=false

# Or install pycarlo:
pip install pycarlo
        """)

def render_sdk_overview(client):
    """Render SDK overview section"""
    st.subheader("📡 Connection & Account Status")
    
    # Connection status with detailed info
    col1, col2 = st.columns([1, 1])
    
    with col1:
        status = client.client.test_connection()
        if status['status'] == 'connected':
            st.success(f"✅ Connected ({status['mode']} mode)")
            st.info(status['message'])
        else:
            st.error(f"❌ Connection failed: {status['message']}")
    
    with col2:
        # Account information
        account_info = client.client.get_account_info()
        st.info("**Account Information**")
        st.write(f"**Account:** {account_info['account_name']}")
        st.write(f"**Tier:** {account_info['tier']}")
        st.write(f"**Account ID:** {account_info['account_id']}")
    
    # Integration status
    st.subheader("🎯 Integration Status")
    integration_status = client.get_integration_status()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mode", integration_status['mode'].title())
    with col2:
        st.metric("Connection", integration_status['connection']['status'].title())
    with col3:
        capabilities = integration_status['capabilities']
        active_features = sum(1 for v in capabilities.values() if v)
        st.metric("Active Features", f"{active_features}/{len(capabilities)}")
    
    # Capabilities matrix
    st.subheader("🛠️ Capabilities")
    capabilities = integration_status['capabilities']
    cap_df = pd.DataFrame([
        {"Feature": k.replace('_', ' ').title(), "Status": "✅ Available" if v else "🔄 Coming Soon"}
        for k, v in capabilities.items()
    ])
    st.dataframe(cap_df, use_container_width=True, hide_index=True)
    
    # Next steps
    st.subheader("🎯 Next Steps")
    next_steps = integration_status['next_steps']
    for i, step in enumerate(next_steps[:3], 1):
        st.write(f"{i}. {step}")

def render_quality_metrics_section(client):
    """Render comprehensive quality metrics section"""
    st.subheader("📊 Quality Dashboard")
    
    # Overall metrics
    metrics = client.client.get_quality_metrics()
    
    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{metrics['overall_score']:.1f}%", 
                 delta=metrics['quality_trends']['improvement'])
    with col2:
        st.metric("Tables Monitored", metrics['tables_monitored'])
    with col3:
        st.metric("Active Incidents", metrics['active_incidents'], delta=-1)
    with col4:
        st.metric("Resolved Issues", metrics['resolved_incidents'], delta=3)
    
    # Quality trends chart
    st.subheader("📈 Quality Trends (Last 7 Days)")
    trend_data = pd.DataFrame({
        'Day': range(1, 8),
        'Quality Score': metrics['quality_trends']['last_7_days']
    })
    st.line_chart(trend_data.set_index('Day'))
    
    # Top issues breakdown
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔍 Issue Types")
        issues_df = pd.DataFrame(metrics['top_issues'])
        if not issues_df.empty:
            st.bar_chart(issues_df.set_index('type'))
    
    with col2:
        st.subheader("📋 Per-Table Quality Scores")
        # Get metrics for each table
        table_names = [
            "product_operations_incidents_2025",
            "business_intelligence_reports_2025", 
            "data_quality_violations_2025",
            "system_monitoring_events_2025",
            "user_behavior_analytics_2025",
            "customer_support_metrics_2025"
        ]
        
        table_metrics = []
        for table in table_names:
            table_data = client.client.get_quality_metrics(table)
            table_metrics.append({
                "Table": table.replace('_2025', '').replace('_', ' ').title(),
                "Score": f"{table_data['quality_score']:.1f}%",
                "Issues": len(table_data['issues'])
            })
        
        table_df = pd.DataFrame(table_metrics)
        st.dataframe(table_df, use_container_width=True, hide_index=True)

def render_incident_management_section(client):
    """Render incident management section"""
    st.subheader("🚨 Incident Management")
    
    # Incident summary
    incidents = client.client.get_incidents(limit=10)
    
    if incidents:
        # Incident stats
        col1, col2, col3 = st.columns(3)
        
        open_incidents = [i for i in incidents if i['status'] == 'investigating']
        resolved_incidents = [i for i in incidents if i['status'] == 'resolved']
        high_severity = [i for i in incidents if i['severity'] == 'high']
        
        with col1:
            st.metric("Open Incidents", len(open_incidents))
        with col2:
            st.metric("Resolved Recently", len(resolved_incidents))
        with col3:
            st.metric("High Severity", len(high_severity))
        
        # Incident details table
        st.subheader("📋 Incident Details")
        
        incident_data = []
        for incident in incidents:
            severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(incident['severity'], "⚪")
            status_icon = {"investigating": "🔍", "resolved": "✅", "open": "🔔"}.get(incident['status'], "❓")
            
            incident_data.append({
                "Severity": f"{severity_icon} {incident['severity'].title()}",
                "Type": incident['type'].replace('_', ' ').title(),
                "Table": incident['table'].replace('_2025', '').replace('_', ' ').title(),
                "Status": f"{status_icon} {incident['status'].title()}",
                "Description": incident['description'][:50] + "..." if len(incident['description']) > 50 else incident['description']
            })
        
        incidents_df = pd.DataFrame(incident_data)
        st.dataframe(incidents_df, use_container_width=True, hide_index=True)
        
        # Incident simulation
        st.subheader("🎭 Incident Simulation")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚨 Simulate Data Quality Alert"):
                st.warning("**Simulated Alert:** Freshness issue detected in customer_support_metrics_2025")
                st.write("• **Threshold:** Data should be < 2 hours old")
                st.write("• **Current Age:** 3.5 hours")
                st.write("• **Recommended Action:** Check ETL pipeline status")
        
        with col2:
            if st.button("✅ Simulate Issue Resolution"):
                st.success("**Simulated Resolution:** Schema change incident marked as resolved")
                st.write("• **Root Cause:** Approved schema migration")
                st.write("• **Resolution Time:** 45 minutes")
                st.write("• **Prevention:** Updated change management process")
    else:
        st.info("No incidents found - excellent data quality! 🎉")

def render_rule_management_section(client):
    """Render rule management section"""
    st.subheader("⚙️ Quality Rule Management")
    
    # Existing rules
    st.subheader("📋 Active Quality Rules")
    rules = client.client.get_quality_rules()
    
    if rules:
        rules_data = []
        for rule in rules:
            rule_data = {
                "Rule ID": rule['rule_id'],
                "Type": rule['type'].title(),
                "Table": rule.get('table', 'All Tables'),
                "Threshold": str(rule.get('threshold', 'N/A')),
                "Status": rule['status']
            }
            rules_data.append(rule_data)
        
        rules_df = pd.DataFrame(rules_data)
        st.dataframe(rules_df, use_container_width=True, hide_index=True)
    else:
        st.info("No quality rules configured")
    
    # Rule creation interface
    st.subheader("➕ Create New Quality Rule")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rule_type = st.selectbox(
            "Rule Type", 
            ["completeness", "uniqueness", "freshness", "validity", "volume", "distribution"],
            help="Select the type of quality check to implement"
        )
        
        table_options = [
            "product_operations_incidents_2025",
            "business_intelligence_reports_2025", 
            "data_quality_violations_2025",
            "system_monitoring_events_2025",
            "user_behavior_analytics_2025",
            "customer_support_metrics_2025",
            "all_tables"
        ]
        table_name = st.selectbox("Target Table", table_options)
        
        if rule_type in ["completeness", "uniqueness", "validity"]:
            threshold = st.slider("Threshold (%)", 0.0, 1.0, 0.95, 0.01)
        elif rule_type == "freshness":
            threshold = st.selectbox("Max Age", ["1 hour", "2 hours", "4 hours", "1 day"])
        else:
            threshold = st.number_input("Threshold Value", value=100)
    
    with col2:
        st.info("**Rule Type Descriptions:**")
        rule_descriptions = {
            "completeness": "Checks for missing/null values",
            "uniqueness": "Ensures no duplicate records", 
            "freshness": "Monitors data recency",
            "validity": "Validates data format/ranges",
            "volume": "Detects unusual row count changes",
            "distribution": "Monitors statistical distribution"
        }
        st.write(f"**{rule_type.title()}:** {rule_descriptions.get(rule_type, 'Custom validation rule')}")
        
        # Advanced options
        with st.expander("Advanced Options"):
            alert_on_failure = st.checkbox("Send Alert on Failure", value=True)
            auto_resolve = st.checkbox("Auto-resolve when fixed", value=False)
            schedule = st.selectbox("Check Frequency", ["Every 15 min", "Hourly", "Daily", "On data change"])
    
    if st.button("🚀 Create Quality Rule", type="primary"):
        rule_config = {
            "type": rule_type,
            "table": table_name if table_name != "all_tables" else None,
            "threshold": threshold,
            "alert_on_failure": alert_on_failure,
            "auto_resolve": auto_resolve,
            "schedule": schedule
        }
        
        rule = client.client.create_quality_rule(rule_config)
        st.success(f"✅ Rule created: {rule['rule_id']}")
        st.info(rule['message'])
        
        # Show rule details
        with st.expander("View Rule Configuration"):
            st.json(rule_config)

def render_api_patterns_section(client):
    """Render API patterns and integration examples"""
    st.subheader("� API Patterns & Integration")
    
    # API capabilities overview
    st.subheader("🛠️ Available API Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**GraphQL Operations**")
        st.write("• Queries for data retrieval")
        st.write("• Mutations for data modification")
        st.write("• Subscriptions for real-time updates")
        st.write("• Schema introspection")
        
        st.info("**Session Management**")
        st.write("• Basic authentication sessions")
        st.write("• Scoped sessions (Airflow, Data Collectors)")
        st.write("• Profile-based authentication")
        st.write("• Environment variable configuration")
    
    with col2:
        st.info("**Direct API Calls**")
        st.write("• Custom endpoint access via make_request()")
        st.write("• Airflow callback integration")
        st.write("• Data collector health checks")
        st.write("• Custom metric ingestion")
        
        st.info("**Integration Patterns**")
        st.write("• CI/CD pipeline integration")
        st.write("• Custom dashboard development")
        st.write("• Automated alerting workflows")
        st.write("• Data quality gates")
    
    # Interactive API testing
    st.subheader("🧪 Interactive API Testing")
    
    # Session scope testing
    scope_options = ["Default", "AirflowCallbacks", "DataCollectors", "MetricIngestion"]
    selected_scope = st.selectbox("Test with Scope", scope_options)
    
    # API endpoint testing
    endpoint_options = {
        "/test/endpoint": "GET",
        "/airflow/callbacks": "POST", 
        "/collectors/health": "GET",
        "/custom-metrics": "POST",
        "/incidents": "GET"
    }
    
    selected_endpoint = st.selectbox("API Endpoint", list(endpoint_options.keys()))
    method = endpoint_options[selected_endpoint]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"🚀 Test {method} {selected_endpoint}"):
            # Create client with specific scope
            scope = None if selected_scope == "Default" else selected_scope
            test_client = MonteCarloIntegration(demo_mode=True, scope=scope)
            
            # Make API call
            if method == "POST" and "metrics" in selected_endpoint:
                body = {"metrics": [{"name": "test_metric", "value": 100}]}
                response = test_client.client.make_request(selected_endpoint, method, body)
            else:
                response = test_client.client.make_request(selected_endpoint, method)
            
            st.success(f"✅ {method} request successful!")
            st.json(response)
    
    with col2:
        if st.button("📊 Get Account Information"):
            account_info = client.client.get_account_info()
            st.success("✅ Account info retrieved!")
            st.json(account_info)
    
    # Code examples
    st.subheader("💻 Code Examples")
    
    example_type = st.selectbox("Example Type", [
        "Basic Client Setup",
        "Session with Scopes", 
        "Quality Rule Creation",
        "Direct API Calls",
        "CI/CD Integration"
    ])
    
    code_examples = {
        "Basic Client Setup": '''
from pycarlo.core import Client, Query, Mutation

# Method 1: Use default profile
client = Client()

# Method 2: Environment variables
from pycarlo.core import Session
session = Session(
    mcd_id=os.getenv("MONTE_CARLO_API_ID"),
    mcd_token=os.getenv("MONTE_CARLO_API_TOKEN")
)
client = Client(session=session)
        ''',
        "Session with Scopes": '''
from pycarlo.core import Session, Client

# Specialized scope for Airflow integration
session = Session(
    mcd_id="your-api-id",
    mcd_token="your-api-token", 
    scope="AirflowCallbacks"
)
client = Client(session=session)

# Make specialized API calls
response = client.make_request("/airflow/callbacks", "POST", {
    "dag_id": "data_pipeline",
    "task_id": "quality_check",
    "status": "success"
})
        ''',
        "Quality Rule Creation": '''
from pycarlo.core import Client, Mutation

client = Client()
mutation = Mutation()

# Create completeness rule
rule_config = {
    "table_id": "your_table_id",
    "rule_type": "completeness",
    "threshold": 0.95,
    "column": "critical_field"
}

# Execute mutation (specific syntax depends on Monte Carlo's schema)
result = client(mutation)
        ''',
        "Direct API Calls": '''
# Using make_request for specialized endpoints
client = Client()

# Health check for data collectors
health = client.make_request("/collectors/health", "GET")

# Submit custom metrics
metrics_data = {
    "metrics": [
        {"name": "custom_quality_score", "value": 0.92},
        {"name": "processing_time", "value": 120}
    ]
}
result = client.make_request("/custom-metrics", "POST", metrics_data)
        ''',
        "CI/CD Integration": '''
# Example CI/CD quality gate
from pycarlo.core import Client

def quality_gate_check():
    client = Client()
    
    # Get current quality metrics
    query = Query()
    query.get_incidents(first=10).__fields__('id', 'status', 'severity')
    incidents = client(query)
    
    # Fail build if high-severity incidents exist
    high_severity = [i for i in incidents.get_incidents if i.severity == 'HIGH']
    
    if high_severity:
        raise Exception(f"Build blocked: {len(high_severity)} high-severity incidents")
    
    print("✅ Quality gate passed")
        '''
    }
    
    st.code(code_examples[example_type], language='python')
    
    # Production deployment guide
    with st.expander("� Production Deployment Guide"):
        st.markdown("""
        ### Production Setup Checklist
        
        1. **Install pycarlo SDK**
           ```bash
           pip install pycarlo>=0.5.0
           ```
        
        2. **Configure Credentials**
           ```bash
           # Option A: Environment variables
           export MONTE_CARLO_API_ID="your-api-id"
           export MONTE_CARLO_API_TOKEN="your-api-token"
           
           # Option B: Monte Carlo CLI
           montecarlo configure
           ```
        
        3. **Update Dashboard Configuration**
           ```python
           # Set demo_mode=False for production
           client = MonteCarloIntegration(demo_mode=False)
           ```
        
        4. **Enable Production Features**
           - Uncomment pycarlo dependencies in requirements.txt
           - Configure real-time alerting
           - Set up CI/CD quality gates
           - Deploy custom monitoring rules
        
        5. **Monitoring & Maintenance**
           - Monitor API rate limits
           - Set up logging and error handling
           - Configure backup authentication methods
           - Regular credential rotation
        """)

def main():
    """Main dashboard application."""
    setup_dashboard()
    
    # Initialize components
    data_manager = DataManager(config.duckdb_path)
    ai_analyzer = AIAnalyzer(config)
    live_monitor = LiveMonitor(data_manager)
    
    # Navigation tabs - add Monte Carlo SDK tab if available
    if MONTE_CARLO_SDK_AVAILABLE:
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔴 Live Monitor", 
            "🤖 AI Analysis", 
            "📊 Data Overview",
            "🔗 Monte Carlo SDK"
        ])
    else:
        tab1, tab2, tab3 = st.tabs(["🔴 Live Monitor", "🤖 AI Analysis", "📊 Data Overview"])
    
    with tab1:
        show_live_monitoring(data_manager, live_monitor, ai_analyzer)
    
    with tab2:
        show_ai_analysis(data_manager, ai_analyzer)
    
    with tab3:
        st.subheader("📊 Database Overview")
        stats = data_manager.get_live_stats()
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", stats['total_records'])
            with col2:
                st.metric("Quality Score", f"{stats['quality_score']:.1f}%")
            with col3:
                st.metric("Issues", stats['null_descriptions'] + stats['short_descriptions'])
            with col4:
                st.metric("Data Freshness", "Real-time")
    
    # Add Monte Carlo SDK tab if available
    if MONTE_CARLO_SDK_AVAILABLE:
        with tab4:
            render_monte_carlo_sdk_tab()

if __name__ == "__main__":
    # Check if running as standalone or as Streamlit app
    if len(sys.argv) > 1 and sys.argv[1] == "load_data":
        # Load data mode
        data_manager = DataManager(config.duckdb_path)
        data_manager.load_csv_files()
    elif len(sys.argv) > 1 and sys.argv[1] == "monitor":
        # Monitor mode
        data_manager = DataManager(config.duckdb_path)
        live_monitor = LiveMonitor(data_manager)
        live_monitor.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            live_monitor.stop_monitoring()
    else:
        # Streamlit dashboard mode
        main()
