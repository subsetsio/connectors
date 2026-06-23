import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su, duckdb, glob
ASSET="clinicaltrials-gov-devtest2"
with su.raw_writer(ASSET,"ndjson.gz",mode="wt",compression="gzip") as fh:
    fh.write(json.dumps({"nct_id":"NCT00000001","n":5})+"\n")
    fh.write(json.dumps({"nct_id":"NCT00000002","n":7})+"\n")
# find the file path the way the runtime would glob it
paths = su.list_raw_files(ASSET) or glob.glob(os.path.join(os.environ.get("SUBSETS_DATA_DIR","data"),"**",ASSET+"*"),recursive=True)
print("listed:", su.list_raw_files(ASSET))
# locate file under data/dev
hits=[]
for root,_,files in os.walk("."):
    for f in files:
        if f.startswith(ASSET): hits.append(os.path.join(root,f))
print("found:", hits)
if hits:
    con=duckdb.connect()
    print(con.execute(f"SELECT nct_id, n FROM read_json_auto('{hits[0]}')").fetchall())
su.delete_raw_file(ASSET,"ndjson.gz")
