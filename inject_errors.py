#!/usr/bin/env python3
"""
Script to inject data quality issues for demonstrating observability features.
This shows how the monitoring system detects and reports various types of data problems.
"""

import duckdb
from config import config
import logging

# Setup logging
logging.basicConfig(level=getattr(logging, config.log_level.upper(), logging.INFO))

def inject_problematic_data():
    """Add records with various data quality issues for testing."""
    
    problematic_records = [
        {
            'title': 'Corrupted Record',
            'description': None,  # NULL value
        },
        {
            'title': 'Empty Content Issue',
            'description': '',  # Empty string
        },
        {
            'title': 'Truncated Data',
            'description': 'This record appears to have been cut off mid-sent',
        },
        {
            'title': 'Special Characters Error',
            'description': '���������� corrupted encoding detected ����������',
        },
        {
            'title': 'Suspicious Pattern',
            'description': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        },
        {
            'title': 'SQL Injection Attempt',
            'description': "'; DROP TABLE users; --",
        },
        {
            'title': 'Malformed JSON',
            'description': '{"incomplete": "json structure without closing brace"',
        },
        {
            'title': 'Extremely Long Title That Exceeds Normal Length Expectations And Could Indicate Data Quality Issues Or Database Schema Problems',
            'description': 'This record has an unusually long title that might indicate a data loading error.',
        }
    ]
    
    try:
        # Connect to database
        con = duckdb.connect(config.duckdb_path)
        
        print("🚨 Injecting problematic data for testing observability...")
        
        # Insert problematic records
        for i, record in enumerate(problematic_records, 1):
            try:
                # Get next ID
                max_id = con.execute("SELECT COALESCE(MAX(id), 0) FROM summarize_model").fetchone()[0]
                new_id = max_id + i
                
                # Calculate description length
                desc_length = len(record['description']) if record['description'] else 0
                
                # Insert record
                con.execute("""
                    INSERT INTO summarize_model (id, title, description, description_length)
                    VALUES (?, ?, ?, ?)
                """, (new_id, record['title'], record['description'], desc_length))
                
                status = "NULL" if record['description'] is None else f"{len(record['description'] or '')} chars"
                print(f"   ✅ Injected record {new_id}: {record['title'][:40]}... ({status})")
                
            except Exception as e:
                print(f"   ❌ Failed to inject record {i}: {e}")
        
        # Check results
        count = con.execute("SELECT COUNT(*) FROM summarize_model").fetchone()[0]
        print(f"✅ Total records in model: {count}")
        
        # Show the problematic records we just added
        problem_records = con.execute("""
            SELECT id, title, description, description_length
            FROM summarize_model 
            WHERE id > ? 
            ORDER BY id DESC
        """, (max_id,)).fetchall()
        
        if problem_records:
            print(f"\n🔍 Recently added problematic records:")
            for record in problem_records:
                desc = record[2] if record[2] else "NULL"
                print(f"   • ID {record[0]}: {record[1][:35]}... -> {desc[:25]}... ({record[3]} chars)")
        
        con.close()
        print(f"\n🎯 Data injection complete! Run 'python ai_layer/summarize.py' to see quality alerts.")
        
    except Exception as e:
        logging.error(f"Error injecting data: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_problematic_data()
