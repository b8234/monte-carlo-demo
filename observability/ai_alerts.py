import os
import subprocess
import logging
from datetime import datetime
import duckdb
from openai import OpenAI
from pathlib import Path
import sys

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import config

logging.basicConfig(level=getattr(logging, config.log_level.upper(), logging.INFO))

def setup_openai_client():
    """Initialize the OpenAI client using centralized config."""
    try:
        client = OpenAI(
            organization=config.openai_organization,
            project=config.openai_project,
            api_key=config.openai_api_key
        )
        return client
    except Exception as e:
        logging.error(f"Error initializing OpenAI client: {e}")
        raise

# Initialize OpenAI client
client = setup_openai_client()

# ----------------------------
# 🧠 CONSTANTS
# ----------------------------
GENERIC_RESPONSES = {
    "i'm sorry", "i don't know", "this is a summary", "summary not available",
    "no content provided", "insufficient information"
}

# ----------------------------
# ✅ DBT TEST RUNNER
# ----------------------------
def run_dbt_tests():
    logging.info("🔎 Running dbt tests...")

    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    dbt_dir = os.path.join(project_root, "dbt_project")

    if not os.path.exists(dbt_dir):
        raise FileNotFoundError(f"❌ Could not find dbt_project folder at: {dbt_dir}")

    logging.info(f"📁 Using dbt directory: {dbt_dir}")

    try:
        result = subprocess.run(
            ["dbt", "test"],
            cwd=dbt_dir,
            capture_output=True,
            text=True,
            check=True
        )

        output_lines = result.stdout.strip().splitlines()
        failing_tests = []

        for line in output_lines:
            # ✅ Only catch real failures — not summary lines
            if line.strip().startswith("FAIL") or line.strip().startswith("ERROR"):
                failing_tests.append({"message": line})

        return failing_tests

    except subprocess.CalledProcessError as e:
        logging.error("❌ dbt test run failed.")
        logging.error(e.stderr)
        return []

# ----------------------------
# 🧠 AI SUMMARY VALIDATION
# ----------------------------
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

def run_ai_quality_checks():
    con = duckdb.connect(config.duckdb_path)
    try:
        rows = con.execute("SELECT id, title, description FROM summarize_model").fetchall()
    except Exception as e:
        raise RuntimeError(f"❌ Failed to read summarize_model: {e}")

    ai_alerts = []
    for row_id, title, description in rows:
        summary = generate_summary(description)

        if summary.startswith("ERROR:"):
            ai_alerts.append((row_id, title, "Summary generation failed"))
        elif not summary.strip():
            ai_alerts.append((row_id, title, "Empty summary"))
        elif len(summary.split()) < 5:
            ai_alerts.append((row_id, title, "Suspiciously short summary"))
        elif any(generic in summary.lower() for generic in GENERIC_RESPONSES):
            ai_alerts.append((row_id, title, "Generic/hallucinated summary"))

    return ai_alerts

# ----------------------------
# 🚨 ALERT LOGIC
# ----------------------------
def simulate_alerts(dbt_failures, ai_failures):
    if not dbt_failures and not ai_failures:
        logging.info("✅ No issues detected in dbt tests or AI output.")
        return

    if dbt_failures:
        logging.warning("🚨 ALERT: Issues detected in dbt tests!")
        for failure in dbt_failures:
            logging.warning(f"🧨 Test Failure: {failure['message']}")

    if ai_failures:
        logging.warning("🚨 ALERT: AI summary quality issues detected!")
        for row_id, title, reason in ai_failures:
            logging.warning(f"⚠️ AI ALERT (row {row_id} - {title}): {reason}")

    logging.info(f"\n🔔 Total issues flagged: {len(dbt_failures) + len(ai_failures)} at {datetime.now().isoformat()}\n")

# ----------------------------
# ▶️ ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    dbt_failures = run_dbt_tests()
    ai_failures = run_ai_quality_checks()
    simulate_alerts(dbt_failures, ai_failures)
