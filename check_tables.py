import duckdb

con = duckdb.connect("monte-carlo.duckdb")  # Adjust path if needed
tables = con.execute("SHOW TABLES").fetchall()

print("📋 Tables in DuckDB:")
for table in tables:
    print("-", table[0])
