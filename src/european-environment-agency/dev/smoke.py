import os, sys, tempfile, duckdb, glob
os.environ["DATA_DIR"]=tempfile.mkdtemp(prefix="eea-smoke-")
sys.path.insert(0, os.path.join(os.getcwd(),"src"))
from nodes.european_environment_agency import fetch_one, _META, _spec_id

# blob table: AirQualityDataFlows.Models (small)
sid=_spec_id("AirQualityDataFlows.Models")
assert sid in _META, "Models not accepted"
print("META:", _META[sid][:2], "blob?", bool(_META[sid][2]))
fetch_one(sid)
f=glob.glob(os.path.join(os.environ["DATA_DIR"],"raw",f"{sid}.ndjson.gz"))
print("wrote:", f)
con=duckdb.connect()
n=con.sql(f"SELECT count(*) FROM read_json_auto('{f[0]}')").fetchone()[0]
cols=con.sql(f"SELECT * FROM read_json_auto('{f[0]}') LIMIT 1").columns
print("blob rows:", n, "ncols:", len(cols), "first cols:", cols[:5])
