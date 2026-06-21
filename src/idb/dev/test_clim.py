import sys
sys.path.insert(0,'src'); sys.path.insert(0,'src/nodes')
import importlib, idb; importlib.reload(idb)
import pyarrow.parquet as pq, glob
for y in ("2016","2017","2018"):
    nid=f"idb-{y}-idb-climate-finance-database"
    idb.fetch_one(nid)
    f=glob.glob(f"data/**/{nid}.parquet", recursive=True)[0]
    t=pq.read_table(f)
    print(f"{y}: rows={t.num_rows} cols={t.column_names[:4]}... src={set(t.column('source_resource').to_pylist())}")
