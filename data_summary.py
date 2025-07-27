"""
Quick data quality summary for the monte-carlo-demo project.
Shows key metrics at a glance.
"""

import duckdb

def show_quick_summary():
    """Display a quick summary of data and quality issues."""
    
    con = duckdb.connect("monte-carlo.duckdb")
    
    print("📊 Monte Carlo Demo - Quick Data Summary")
    print("=" * 50)
    
    try:
        # Total records across main data tables
        total_query = """
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT CASE WHEN description IS NOT NULL THEN id END) as records_with_description,
                COUNT(DISTINCT CASE WHEN description IS NULL OR description = '' THEN id END) as problematic_records
            FROM (
                SELECT id, description FROM raw_data
                UNION ALL
                SELECT id, description FROM generated_sample
                UNION ALL
                SELECT id, description FROM problematic_data
                UNION ALL
                SELECT id, description FROM additional_data
                UNION ALL
                SELECT id, description FROM enriched_data
            )
        """
        
        result = con.execute(total_query).fetchone()
        total, with_desc, problematic = result
        
        print(f"📈 Total Records: {total}")
        print(f"✅ With Valid Descriptions: {with_desc}")
        print(f"⚠️  Problematic Records: {problematic}")
        print(f"📊 Quality Rate: {(with_desc/total*100):.1f}%")
        
        # Sample problematic records for demo
        print(f"\n🎯 Sample Issues for Demo:")
        samples = con.execute("""
            SELECT table_name, id, title, 
                   CASE 
                       WHEN description IS NULL THEN '[NULL]'
                       WHEN description = '' THEN '[EMPTY]'
                       ELSE LEFT(description, 30) || '...'
                   END as issue_desc
            FROM (
                SELECT 'raw_data' as table_name, id, title, description FROM raw_data
                UNION ALL
                SELECT 'problematic_data' as table_name, id, title, description FROM problematic_data
            )
            WHERE description IS NULL 
               OR description = ''
               OR LENGTH(TRIM(description)) < 5
            LIMIT 5
        """).fetchall()
        
        for sample in samples:
            print(f"   - {sample[0]}.{sample[1]}: {sample[2]} -> {sample[3]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        con.close()

if __name__ == "__main__":
    show_quick_summary()
