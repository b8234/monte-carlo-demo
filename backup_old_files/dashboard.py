import os
import duckdb
import streamlit as st
import time
from openai import OpenAI
from datetime import datetime
from config import config

# OpenAI setup
try:
    client = OpenAI(
        organization=config.openai_organization,
        project=config.openai_project,
        api_key=config.openai_api_key
    )
except ValueError as e:
    st.error(f"Configuration error: {e}")
    st.error("Please check your .env file and ensure all required OpenAI credentials are set.")
    st.stop()

# Generic responses to detect weak AI summaries
GENERIC_RESPONSES = {
    "i'm sorry", "i don't know", "this is a summary", "summary not available",
    "no content provided", "insufficient information"
}

# Load data
DB_PATH = config.duckdb_path
con = duckdb.connect(DB_PATH)

def get_live_stats():
    """Get current database statistics for live monitoring."""
    try:
        con = duckdb.connect(config.duckdb_path)
        
        # Total records
        total_records = con.execute("SELECT COUNT(*) FROM summarize_model").fetchone()[0]
        
        # Records added in last 5 minutes (approximate)
        recent_records = con.execute("""
            SELECT COUNT(*) FROM summarize_model 
            WHERE id > (SELECT MAX(id) - 10 FROM summarize_model)
        """).fetchone()[0]
        
        # Quality metrics
        null_descriptions = con.execute("""
            SELECT COUNT(*) FROM summarize_model 
            WHERE description IS NULL OR description = ''
        """).fetchone()[0]
        
        short_descriptions = con.execute("""
            SELECT COUNT(*) FROM summarize_model 
            WHERE description_length < 10 AND description IS NOT NULL
        """).fetchone()[0]
        
        con.close()
        
        return {
            'total_records': total_records,
            'recent_records': recent_records,
            'null_descriptions': null_descriptions,
            'short_descriptions': short_descriptions,
            'quality_score': ((total_records - null_descriptions - short_descriptions) / total_records * 100) if total_records > 0 else 0
        }
    except Exception as e:
        st.error(f"Error getting live stats: {e}")
        return None

def show_live_monitoring():
    """Display live monitoring section."""
    st.subheader("🔴 Live Demo Monitor")
    
    # Auto-refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        auto_refresh = st.checkbox("🔄 Auto-refresh (10 seconds)", value=False)
    
    with col2:
        if st.button("📊 Refresh Now"):
            st.rerun()
    
    with col3:
        if st.button("🎬 Demo Guide"):
            st.info("""
            **Live Demo Instructions:**
            1. Start live monitor: `python live_demo_monitor.py`
            2. Drop CSV files in the `demo/` folder
            3. Watch real-time updates here!
            
            **Sample files available:**
            - `demo/sample_mixed_quality.csv`
            - `demo/sample_critical_issues.csv` 
            - `demo/sample_good_quality.csv`
            """)
    
    # Get live statistics
    stats = get_live_stats()
    if stats:
        # Display metrics
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
    
    # Show recent records
    st.subheader("📋 Recent Records")
    try:
        con = duckdb.connect(config.duckdb_path)
        recent_data = con.execute("""
            SELECT id, title, description, description_length
            FROM summarize_model 
            ORDER BY id DESC 
            LIMIT 10
        """).fetchdf()
        
        if not recent_data.empty:
            # Add quality indicators
            recent_data['Quality'] = recent_data.apply(lambda row: 
                "🚨 NULL" if row['description'] is None or row['description'] == '' 
                else "⚠️ SHORT" if row['description_length'] < 10 
                else "✅ OK", axis=1)
            
            st.dataframe(recent_data[['id', 'title', 'Quality', 'description_length']], use_container_width=True)
        else:
            st.info("No records found")
        
        con.close()
    except Exception as e:
        st.error(f"Error loading recent records: {e}")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(10)
        st.rerun()

# Helper: Generate AI summary
@st.cache_data(show_spinner=False)
def generate_summary(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes content."},
                {"role": "user", "content": f"Summarize this:\n\n{text}"}
            ],
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {e}"

# Helper: Run AI summary validation
@st.cache_data(show_spinner=True)
def run_ai_checks(rows):
    ai_alerts = []
    summaries = []

    for row_id, title, description in rows:
        summary = generate_summary(description)

        reason = None
        if summary.startswith("ERROR:"):
            reason = "Summary generation failed"
        elif not summary.strip():
            reason = "Empty summary"
        elif len(summary.split()) < 5:
            reason = "Suspiciously short summary"
        elif any(resp in summary.lower() for resp in GENERIC_RESPONSES):
            reason = "Generic/hallucinated summary"

        summaries.append((row_id, title, description, summary, reason))
        if reason:
            ai_alerts.append((row_id, title, reason))

    return summaries, ai_alerts

# Layout
st.set_page_config(page_title="Monte Carlo Demo Dashboard", layout="wide")
st.title("📊 Monte Carlo Observability Demo")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Navigation tabs
tab1, tab2, tab3 = st.tabs(["🔴 Live Demo Monitor", "📊 Data Analysis", "📋 Full Report"])

with tab1:
    show_live_monitoring()

with tab2:
    st.subheader("📊 Data Analysis Overview")
    
    # Quick stats
    stats = get_live_stats()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", stats['total_records'])
        with col2:
            st.metric("Quality Score", f"{stats['quality_score']:.1f}%")
        with col3:
            st.metric("NULL Values", stats['null_descriptions'])
        with col4:
            st.metric("Short Content", stats['short_descriptions'])

with tab3:
    st.subheader("📋 Complete Analysis Report")
    
    # Load summarize_model
    try:
        rows = con.execute("SELECT id, title, description FROM summarize_model").fetchall()
    except Exception as e:
        st.error(f"Failed to load summarize_model: {e}")
        st.stop()

    # Run AI check
    with st.spinner("🔍 Evaluating AI summaries..."):
        summaries, ai_alerts = run_ai_checks(rows)

    # Simulated dbt failures (from logs or manual example)
    dbt_failures = [
        {"message": "FAIL 1 of 1 not_null_summarize_model_description"}
    ] if "description" in [col[0] for col in con.execute("PRAGMA table_info('summarize_model')").fetchall()] else []

    # 🔴 Section: dbt Failures
    st.subheader("🔴 dbt Test Failures")
    if dbt_failures:
        for fail in dbt_failures:
            st.warning(fail["message"])
    else:
        st.success("No dbt test failures found.")

    # 🟠 Section: AI Alerts
    st.subheader("🟠 AI Summary Quality Issues")
    if ai_alerts:
        for row_id, title, reason in ai_alerts:
            st.error(f"Row {row_id} - {title}: {reason}")
    else:
        st.success("No AI summary issues detected.")

    # 📋 Section: Full Table View
    st.subheader("📋 Summarize Model Output")
    st.dataframe(
        {
            "ID": [row[0] for row in summaries],
            "Title": [row[1] for row in summaries],
            "Description": [row[2] for row in summaries],
            "Summary": [row[3] for row in summaries],
            "Issue": [row[4] if row[4] else "✅" for row in summaries]
        },
        use_container_width=True
    )
