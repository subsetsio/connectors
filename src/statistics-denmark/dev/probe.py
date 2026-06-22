import csv
import pyarrow as pa
import duckdb
from subsets_utils import get, get_client

table_id = "ABST1"
info = get(f"https://api.statbank.dk/v1/tableinfo/{table_id}", params={"format": "JSON", "lang": "en"}).json()
body = {"table": table_id, "format": "BULK", "lang": "en",
        "variables": [{"code": v["id"], "values": ["*"]} for v in info["variables"]]}

client = get_client()
rows = []
with client.stream("POST", "https://api.statbank.dk/v1/data", json=body, timeout=600) as resp:
    resp.raise_for_status()
    reader = csv.reader(resp.iter_lines(), delimiter=";")
    header = [c.strip() for c in next(reader)]
    for r in reader:
        if not r or (len(r) == 1 and r[0] == ""):
            continue
        rows.append(r)

print("header:", header)
print("nrows:", len(rows))
ncol = len(header)
schema = pa.schema([(c, pa.string()) for c in header])
cols = [pa.array([row[j] if j < len(row) else None for row in rows], type=pa.string()) for j in range(ncol)]
tbl = pa.record_batch(cols, schema=schema)
t = pa.Table.from_batches([tbl])

con = duckdb.connect()
con.register("asset", t)
sql = """
    SELECT * EXCLUDE (INDHOLD),
           TRY_CAST(NULLIF(NULLIF(TRIM(INDHOLD), '..'), '.') AS DOUBLE) AS value
    FROM asset
"""
out = con.execute(sql).arrow()
print("transform cols:", out.column_names)
print("transform rows:", out.num_rows)
print("value nulls:", out.column("value").null_count)
print(out.slice(0, 3).to_pylist())
