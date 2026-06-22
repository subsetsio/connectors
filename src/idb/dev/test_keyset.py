import sys
sys.path.insert(0,'src'); sys.path.insert(0,'src/nodes')
import importlib, idb; importlib.reload(idb)
import pyarrow.parquet as pq, glob
# small datastore pkg + one LMW (multi-resource, ~few hundred k rows)
for nid in ["idb-2016-idb-climate-finance-database","idb-risk-monitor"]:
    idb.fetch_one(nid)
    f=glob.glob(f"data/**/{nid}.parquet", recursive=True)[0]
    t=pq.read_table(f)
    print(f"{nid}: rows={t.num_rows} ncols={len(t.column_names)}", flush=True)
# verify climate vs datastore total
rec=idb._api("package_show", id="2016-idb-climate-finance-database")
