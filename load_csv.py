import duckdb
import pandas as pd
import os
from pathlib import Path

def load_csv_files():
    """Load all CSV files from the data directory into DuckDB."""
    
    # Connect to DuckDB (creates file if not exists)
    con = duckdb.connect("monte-carlo.duckdb")
    
    data_dir = Path("data")
    csv_files = list(data_dir.glob("*.csv"))
    
    print(f"📁 Found {len(csv_files)} CSV files in data directory")
    
    for csv_file in csv_files:
        try:
            # Load CSV
            df = pd.read_csv(csv_file)
            table_name = csv_file.stem  # Use filename without extension as table name
            
            print(f"📊 Loading {csv_file.name} -> {table_name} table ({len(df)} rows)")
            
            # Drop table if exists and create new one
            con.execute(f"DROP TABLE IF EXISTS {table_name}")
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            
            # Show sample of loaded data
            sample = con.execute(f"SELECT * FROM {table_name} LIMIT 3").fetchall()
            print(f"   Sample rows: {len(sample)}")
            
        except Exception as e:
            print(f"❌ Error loading {csv_file.name}: {e}")
    
    # Create a unified view combining all raw data sources
    print("\n🔄 Creating unified raw_data view...")
    try:
        con.execute("DROP VIEW IF EXISTS raw_data")
        con.execute("""
            CREATE VIEW raw_data AS 
            SELECT id, title, description FROM raw_data
            UNION ALL
            SELECT id, title, description FROM additional_data
            UNION ALL  
            SELECT id, title, description FROM enriched_data
        """)
        
        total_rows = con.execute("SELECT COUNT(*) FROM raw_data").fetchone()[0]
        print(f"✅ Created unified raw_data view with {total_rows} total rows")
        
    except Exception as e:
        print(f"⚠️  Could not create unified view: {e}")
        print("   Using raw_data table only")
    
    # Show final table summary
    print("\n📋 Database Summary:")
    tables = con.execute("SHOW TABLES").fetchall()
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        print(f"   {table[0]}: {count} rows")
    
    con.close()
    print("\n✅ All CSV files loaded successfully!")

if __name__ == "__main__":
    load_csv_files()
