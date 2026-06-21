import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
# dev mode: CI unset -> writes to data/dev
os.environ.pop("CI", None)
import nodes.bts as m
import duckdb, glob, json

code_spec = "bts-kki"
m.fetch_one(code_spec)

# find produced raw files
raw_root = os.path.join(os.path.dirname(__file__), "..", "data")
files = glob.glob(os.path.join(raw_root, "**", f"{code_spec}-*.ndjson.gz"), recursive=True)
print("RAW FILES:", files)
assert files, "no raw files produced"
# run the transform SQL locally over the produced ndjson
con = duckdb.connect()
con.execute(f'CREATE VIEW "{code_spec}" AS SELECT * FROM read_json_auto({files!r})')
sql = f'SELECT CAST(obs_date AS DATE) AS date, * EXCLUDE (obs_date) FROM "{code_spec}" WHERE obs_date IS NOT NULL'
res = con.execute(sql)
cols = [d[0] for d in res.description]
rows = res.fetchall()
print("TRANSFORM ncols", len(cols), "rows", len(rows))
print("cols[:8]", cols[:8])
print("sample row[:6]", rows[0][:6] if rows else None)
print("distinct dates", con.execute(f'SELECT DISTINCT date FROM ({sql}) ORDER BY 1').fetchall())
