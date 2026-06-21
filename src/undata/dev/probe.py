"""Validate streaming parse + transform SQL on one small dataflow."""
import csv, json, io, gzip
import duckdb
from subsets_utils import get_client

BASE = "https://data.un.org/ws/rest"
ACCEPT = "application/vnd.sdmx.data+csv"
DF = "DF_UNData_UNFCC"

client = get_client()
out = io.StringIO()
import httpx
with client.stream("GET", f"{BASE}/data/{DF}/all", headers={"Accept": ACCEPT},
                   timeout=httpx.Timeout(30.0, read=600.0)) as resp:
    resp.raise_for_status()
    reader = csv.reader(resp.iter_lines())
    header = next(reader)
    ncols = len(header)
    n = 0
    for row in reader:
        rec = {header[i]: (row[i] if i < len(row) and row[i] != "" else None) for i in range(ncols)}
        out.write(json.dumps(rec, separators=(",", ":")) + "\n")
        n += 1

print("header:", header)
print("rows parsed:", n)

# write gz and run the transform SQL exactly as the runtime would
path = "/tmp/undata_probe.ndjson.gz"
with gzip.open(path, "wt") as f:
    f.write(out.getvalue())

duckdb.sql(f"CREATE OR REPLACE TEMP VIEW v AS SELECT * FROM read_json_auto('{path}')")
res = duckdb.sql('''
    SELECT * EXCLUDE (OBS_VALUE), TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
    FROM v WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
''')
print("transform columns:", res.columns)
print("transform row count:", duckdb.sql("SELECT count(*) FROM ("+res.sql_query()+")").fetchone() if hasattr(res,'sql_query') else 'n/a')
df = res.fetchnumpy()
print("obs_value sample:", list(df['obs_value'][:5]))
print("transform rows:", len(df['obs_value']))
