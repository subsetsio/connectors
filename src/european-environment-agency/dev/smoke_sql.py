import os, sys, tempfile, duckdb, glob, time
os.environ["DATA_DIR"]=tempfile.mkdtemp(prefix="eea-smokesql-")
sys.path.insert(0, os.path.join(os.getcwd(),"src"))
from nodes.european_environment_agency import fetch_one, _META, _spec_id
sid=_spec_id("StatisticalData.eea_s_wat009")
assert sid in _META, "not accepted"
print("META:", _META[sid][:2], "blob?", bool(_META[sid][2]))
t0=time.time()
fetch_one(sid)
print("fetch took %.1fs" % (time.time()-t0))
f=glob.glob(os.path.join(os.environ["DATA_DIR"],"raw",f"{sid}.ndjson.gz"))[0]
con=duckdb.connect()
n=con.sql(f"SELECT count(*) FROM read_json_auto('{f}')").fetchone()[0]
r=con.sql(f"SELECT * FROM read_json_auto('{f}') LIMIT 1")
print("SQL-path rows:", n, "cols:", r.columns)
print("types:", [(c,str(t)) for c,t in zip(r.columns, r.types)])
