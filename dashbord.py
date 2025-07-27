import os
import duckdb
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# OpenAI setup
client = OpenAI(
    organization=os.getenv("OPENAI_ORGANIZATION"),
    project=os.getenv("OPENAI_PROJECT"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Generic responses to detect weak AI summaries
GENERIC_RESPONSES = {
    "i'm sorry", "i don't know", "this is a summary", "summary not available",
    "no content provided", "insufficient information"
}

# Load data
DB_PATH = os.getenv("DUCKDB_PATH", "monte-carlo.duckdb")
con = duckdb.connect(DB_PATH)

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
