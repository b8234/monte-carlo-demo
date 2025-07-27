import duckdb
import pandas as pd

# Load raw CSV
df = pd.read_csv("data/raw_data.csv")

# Connect to DuckDB (creates file if not exists)
con = duckdb.connect("monte-carlo.duckdb")

# Write to table
con.execute("DROP TABLE IF EXISTS raw_data")
con.execute("CREATE TABLE raw_data AS SELECT * FROM df")

print("✅ CSV loaded into DuckDB as table: raw_data")
