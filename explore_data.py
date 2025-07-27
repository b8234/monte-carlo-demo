"""
Data exploration utility for the monte-carlo-demo project.
Provides insights into the loaded sample data and quality issues.
"""

import duckdb
import pandas as pd
from collections import Counter

def explore_data():
    """Explore all loaded data and provide quality insights."""
    
    print("🔍 Monte Carlo Demo - Data Exploration Report")
    print("=" * 60)
    
    # Connect to database
    con = duckdb.connect("monte-carlo.duckdb")
    
    # Get all tables
    tables = con.execute("SHOW TABLES").fetchall()
    print(f"\n📊 Found {len(tables)} tables in database:")
    
    total_records = 0
    quality_issues = []
    
    for table in tables:
        table_name = table[0]
        
        # Get table info
        try:
            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            total_records += count
            print(f"\n🔹 {table_name}: {count} records")
            
            # Analyze quality issues if it has description column
            columns = [col[0] for col in con.execute(f"PRAGMA table_info('{table_name}')").fetchall()]
            
            if 'description' in columns:
                # Check for various quality issues
                null_count = con.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE description IS NULL"
                ).fetchone()[0]
                
                empty_count = con.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE description = ''"
                ).fetchone()[0]
                
                short_count = con.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE LENGTH(description) < 10 AND description IS NOT NULL"
                ).fetchone()[0]
                
                long_count = con.execute(
                    f"SELECT COUNT(*) FROM {table_name} WHERE LENGTH(description) > 500"
                ).fetchone()[0]
                
                print(f"   📋 Quality Analysis:")
                print(f"      - NULL descriptions: {null_count}")
                print(f"      - Empty descriptions: {empty_count}")
                print(f"      - Short descriptions (<10 chars): {short_count}")
                print(f"      - Long descriptions (>500 chars): {long_count}")
                
                quality_issues.extend([
                    ('null_description', null_count),
                    ('empty_description', empty_count),
                    ('short_description', short_count),
                    ('long_description', long_count)
                ])
                
                # Show some sample problematic records
                problematic = con.execute(f"""
                    SELECT id, title, description 
                    FROM {table_name} 
                    WHERE description IS NULL 
                       OR description = '' 
                       OR LENGTH(description) < 10
                    LIMIT 3
                """).fetchall()
                
                if problematic:
                    print(f"   ⚠️  Sample problematic records:")
                    for record in problematic:
                        desc = record[2] if record[2] else "[NULL]"
                        if len(desc) > 50:
                            desc = desc[:47] + "..."
                        print(f"      ID {record[0]}: {record[1]} -> '{desc}'")
            
        except Exception as e:
            print(f"   ❌ Error analyzing {table_name}: {e}")
    
    # Overall summary
    print(f"\n📈 Overall Data Summary:")
    print(f"   Total records across all tables: {total_records}")
    
    # Quality issues summary
    issue_totals = {}
    for issue_type, count in quality_issues:
        issue_totals[issue_type] = issue_totals.get(issue_type, 0) + count
    
    print(f"\n⚠️  Quality Issues Summary:")
    for issue_type, total in issue_totals.items():
        if total > 0:
            percentage = (total / total_records) * 100
            print(f"   - {issue_type.replace('_', ' ').title()}: {total} ({percentage:.1f}%)")
    
    # Show some interesting records
    print(f"\n🎯 Sample Data for Testing:")
    
    try:
        # Find records with special characters
        special_chars = con.execute("""
            SELECT table_name, id, title, LEFT(description, 60) as sample_desc
            FROM (
                SELECT 'raw_data' as table_name, id, title, description FROM raw_data
                UNION ALL
                SELECT 'generated_sample' as table_name, id, title, description FROM generated_sample
            )
            WHERE description LIKE '%€%' 
               OR description LIKE '%🚀%'
               OR description LIKE '%à%'
            LIMIT 3
        """).fetchall()
        
        if special_chars:
            print(f"   📝 Records with special characters:")
            for record in special_chars:
                print(f"      {record[0]}.{record[1]}: {record[2]} -> {record[3]}...")
    
    except Exception as e:
        print(f"   ⚠️  Could not analyze special characters: {e}")
    
    # Test AI scenarios
    print(f"\n🤖 AI Testing Scenarios Available:")
    try:
        # Count different types of content for AI testing
        scenarios = con.execute("""
            SELECT 
                SUM(CASE WHEN description IS NULL OR description = '' THEN 1 ELSE 0 END) as empty_content,
                SUM(CASE WHEN LENGTH(description) < 10 AND description IS NOT NULL THEN 1 ELSE 0 END) as minimal_content,
                SUM(CASE WHEN description LIKE '%TBD%' OR description LIKE '%TODO%' THEN 1 ELSE 0 END) as placeholder_content,
                SUM(CASE WHEN LENGTH(description) > 200 THEN 1 ELSE 0 END) as rich_content
            FROM (
                SELECT description FROM raw_data
                UNION ALL
                SELECT description FROM generated_sample WHERE description IS NOT NULL
            )
        """).fetchone()
        
        print(f"   - Empty content (will fail AI processing): {scenarios[0]} records")
        print(f"   - Minimal content (may produce poor summaries): {scenarios[1]} records")
        print(f"   - Placeholder content (likely to trigger alerts): {scenarios[2]} records")
        print(f"   - Rich content (good for AI processing): {scenarios[3]} records")
        
    except Exception as e:
        print(f"   ⚠️  Could not analyze AI scenarios: {e}")
    
    con.close()
    
    print(f"\n✅ Data exploration complete!")
    print(f"\n💡 Next steps:")
    print(f"   1. Run: streamlit run dashboard.py")
    print(f"   2. Check: python observability/alerts.py")
    print(f"   3. Test: python ai_layer/summarize.py")

if __name__ == "__main__":
    explore_data()
