import os
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def run_dbt_tests():
    """Run dbt tests and return a list of failing test messages."""
    logging.info("🔎 Running dbt tests...")

    # Resolve absolute path to dbt_project directory
    current_script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_script_path))
    dbt_dir = os.path.join(project_root, "dbt_project")

    if not os.path.exists(dbt_dir):
        raise FileNotFoundError(f"❌ Could not find dbt_project folder at: {dbt_dir}")

    logging.info(f"📁 Using dbt directory: {dbt_dir}")

    try:
        # Run dbt tests without --output flag
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
            if "FAIL" in line or "ERROR" in line:
                failing_tests.append({
                    "message": line
                })

        return failing_tests

    except subprocess.CalledProcessError as e:
        logging.error("❌ dbt test run failed.")
        logging.error(e.stderr)
        return []


def simulate_alerts(failures):
    """Simulate Monte Carlo-style alerts."""
    if not failures:
        logging.info("✅ No issues detected in dbt tests.")
        return

    logging.warning("🚨 ALERT: Issues detected in dbt tests!")

    for failure in failures:
        logging.warning(f"🧨 Test Failure: {failure['message']}")

    # Simulated alert footer
    from datetime import datetime
    print(f"\n🔔 {len(failures)} data quality issues flagged at {datetime.now().isoformat()}")
    print("Review test logs and upstream models for breakage.\n")


if __name__ == "__main__":
    test_failures = run_dbt_tests()
    simulate_alerts(test_failures)
