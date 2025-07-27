import os
import duckdb
import logging
from openai import OpenAI
from pathlib import Path
import sys

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent.parent))
from config import config

# Setup logging
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

def generate_summary(client, text):
    """Generate a concise summary from OpenAI and detect data quality issues."""
    try:
        response = client.chat.completions.create(
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
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            logging.warning("No content returned from OpenAI")
            return "No summary provided. | DATA QUALITY: ERROR - No AI response"
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return f"Error: {e} | DATA QUALITY: ERROR - API failure"

def main():
    """Main function to demonstrate AI summarization with data quality monitoring."""
    try:
        client = setup_openai_client()
        
        # Use config for database path
        db_path = config.duckdb_path
        con = duckdb.connect(db_path)
        
        rows = con.execute("SELECT id, title, description FROM summarize_model").fetchall()
        print(f"🔎 Found {len(rows)} rows to summarize...\n")

        quality_issues = []
        total_errors = 0
        total_warnings = 0

        for row in rows:
            id, title, description = row
            print(f"\n📝 Analysis for '{title}':")
            result = generate_summary(client, description)
            
            # Parse the result for quality indicators
            if " | DATA QUALITY: " in result:
                summary_part, quality_part = result.split(" | DATA QUALITY: ", 1)
                print(f"   Summary: {summary_part}")
                
                if quality_part.startswith("ERROR"):
                    print(f"   🚨 {quality_part}")
                    quality_issues.append(f"ERROR in '{title}': {quality_part}")
                    total_errors += 1
                elif quality_part.startswith("WARNING"):
                    print(f"   ⚠️  {quality_part}")
                    quality_issues.append(f"WARNING in '{title}': {quality_part}")
                    total_warnings += 1
                else:
                    print(f"   ✅ {quality_part}")
            else:
                print(f"   {result}")
        
        # Summary report
        print(f"\n" + "="*60)
        print(f"🎯 DATA QUALITY REPORT")
        print(f"="*60)
        print(f"📊 Total Records Analyzed: {len(rows)}")
        print(f"🚨 Errors Found: {total_errors}")
        print(f"⚠️  Warnings Found: {total_warnings}")
        print(f"✅ Quality Score: {((len(rows) - total_errors) / len(rows) * 100):.1f}%")
        
        if quality_issues:
            print(f"\n🔍 DETAILED ISSUES:")
            for issue in quality_issues:
                print(f"   • {issue}")
        else:
            print(f"\n🎉 No quality issues detected!")
            
        con.close()
        
    except Exception as e:
        logging.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
