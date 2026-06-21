import duckdb, json, tempfile, os
td = tempfile.mkdtemp()
f1 = os.path.join(td,"a.ndjson"); f2 = os.path.join(td,"b.ndjson")
open(f1,"w").write(json.dumps({"ano":1985,"colA":"x","colB":"y"})+"\n")
open(f2,"w").write(json.dumps({"ano":2023,"colC":"z","colA":"w"})+"\n")
print("--- default read_json_auto over both ---")
try:
    print(duckdb.sql(f"SELECT * FROM read_json_auto(['{f1}','{f2}'])").fetchall())
    print("cols:", duckdb.sql(f"SELECT * FROM read_json_auto(['{f1}','{f2}'])").columns)
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:200])
print("--- with union_by_name ---")
try:
    print(duckdb.sql(f"SELECT * FROM read_json_auto(['{f1}','{f2}'], union_by_name=true)").fetchall())
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:200])
