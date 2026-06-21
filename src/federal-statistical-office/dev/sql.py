import duckdb
sid="federal-statistical-office-px-x-1304070000-101"
path="data/dev/raw/"+sid+".ndjson.gz"
# mimic transform: view named after dep id, then SELECT
duckdb.sql(f'CREATE TEMP VIEW "{sid}" AS SELECT * FROM read_json_auto(\'{path}\')')
sql=f'SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value FROM "{sid}"'
print(duckdb.sql(sql).limit(3))
print("count:", duckdb.sql(f"SELECT count(*) FROM ({sql})").fetchone()[0])
print("value stats:", duckdb.sql(f"SELECT min(value),max(value),count(*) FROM ({sql})").fetchone())
