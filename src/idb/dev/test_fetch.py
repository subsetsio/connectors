import sys
sys.path.insert(0,'src'); sys.path.insert(0,'src/nodes')
import idb
import pyarrow.parquet as pq, glob
nid="idb-2016-idb-climate-finance-database"
print("=== fetching", nid, flush=True)
idb.fetch_one(nid)
for f in glob.glob("data/**/idb-2016-idb-climate-finance-database.parquet", recursive=True):
    t=pq.read_table(f)
    print("file:", f, "rows:", t.num_rows, "cols:", t.column_names, flush=True)
    print(t.slice(0,2).to_pylist(), flush=True)
