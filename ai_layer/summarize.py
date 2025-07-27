import os
import duckdb
import logging
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load .env if you’re using one
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

def refresh_env():
    """Stub: Reload or patch any env-specific logic here (optional)."""
    pass  # You can hook in reloading logic if needed

def load_and_validate_env_vars():
    """Loads and validates critical environment variables."""
    refresh_env()
    required_vars = ["OPENAI_ORGANIZATION", "OPENAI_PROJECT", "OPENAI_API_KEY"]

    env_vars = {var: os.getenv(var) for var in required_vars}
    missing = [k for k, v in env_vars.items() if not v]

    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return env_vars

def setup_openai_client(organization, project, api_key):
    """Initialize the OpenAI client."""
    try:
        client = OpenAI(
            organization=organization,
            project=project,
            api_key=api_key
        )
        return client
    except Exception as e:
        logging.error(f"Error initializing OpenAI client: {e}")
        raise

def generate_summary(client, text):
    """Generate a concise summary from OpenAI."""
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
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            logging.warning("No content returned from OpenAI")
            return "No summary provided."
    except client.error.APIError as api_error:
        logging.error(f"OpenAI API error: {api_error}")
        return f"OpenAI API error: {api_error}"
    except client.error.RateLimitError:
        logging.warning("Rate limit exceeded.")
        return "Rate limit exceeded. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

def main():
    env_vars = load_and_validate_env_vars()
    client = setup_openai_client(
        organization=env_vars["OPENAI_ORGANIZATION"],
        project=env_vars["OPENAI_PROJECT"],
        api_key=env_vars["OPENAI_API_KEY"]
    )

    con = duckdb.connect("../monte-carlo.duckdb")
    rows = con.execute("SELECT id, title, description FROM summarize_model").fetchall()
    print(f"🔎 Found {len(rows)} rows to summarize...\n")

    for row in rows:
        id, title, description = row
        print(f"\n📝 Summary for '{title}':")
        result = generate_summary(client, description)
        print(result)

if __name__ == "__main__":
    main()
