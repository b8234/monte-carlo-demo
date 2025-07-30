#!/usr/bin/env python3
"""
Monte Carlo Data Observability Dashboard - All-in-One
Consolidates: dashboard, live monitoring, AI analysis, data loading, and configuration
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

# ==========================================
# CONFIGURATION MANAGEMENT
# ==========================================

class Config:
    """Centralized configuration management."""
    
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
    """Handles all database operations and data loading."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
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
        """Get current database statistics."""
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
    """Handles AI-powered data quality analysis."""
    
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
    """Handles real-time file monitoring."""
    
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
    """Handle new CSV files."""
    
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

def main():
    """Main dashboard application."""
    setup_dashboard()
    
    # Initialize components
    data_manager = DataManager(config.duckdb_path)
    ai_analyzer = AIAnalyzer(config)
    live_monitor = LiveMonitor(data_manager)
    
    # Navigation tabs
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
