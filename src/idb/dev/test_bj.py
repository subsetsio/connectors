import sys
sys.path.insert(0,'src'); sys.path.insert(0,'src/nodes')
import importlib, idb; importlib.reload(idb)
import pyarrow.parquet as pq, glob
nid="idb-2020-better-jobs-index-database-latin-america"
idb.fetch_one(nid)
for f in glob.glob("data/**/idb-2020-better-jobs-index-database-latin-america.parquet", recursive=True):
    t=pq.read_table(f); print("rows:", t.num_rows, "ncols:", len(t.column_names))
    print("cols:", t.column_names[:12])
    print(t.slice(0,2).to_pylist())
