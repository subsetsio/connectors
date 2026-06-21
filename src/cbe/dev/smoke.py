import sys; sys.path.insert(0,'src')
import os; os.environ.pop("CI",None)
import duckdb
from subsets_utils import load_raw_parquet, list_raw_files
import nodes.cbe as m

# small dataset: net-balancing-item
sid="cbe-banking-survey--net-balancing-item"
m.fetch_one(sid)
t=load_raw_parquet(sid)
print("RAW rows",len(t),"cols",t.column_names)
print("dtypes",[(f.name,str(f.type)) for f in t.schema])
print("null dates",t.column("date").null_count,"null values",t.column("value").null_count)
# run transform SQL via duckdb over the raw file(s)
files=list_raw_files(sid)
print("raw files",files[:2], "...", len(files))
con=duckdb.connect()
# register view named after dep id
import glob
con.execute(f"CREATE VIEW \"{sid}\" AS SELECT * FROM read_parquet({files!r})")
res=con.execute(m._transform_sql(sid)).arrow()
print("TRANSFORM rows",len(res),"cols",res.column_names)
print(res.slice(0,4).to_pylist())
