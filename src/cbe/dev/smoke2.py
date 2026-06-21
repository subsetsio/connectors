import sys; sys.path.insert(0,'src')
import os; os.environ.pop("CI",None)
import duckdb, collections
from subsets_utils import load_raw_parquet
import nodes.cbe as m
def run(sid, fetch=False):
    if fetch: m.fetch_one(sid)
    t=load_raw_parquet(sid)
    con=duckdb.connect(); con.register(sid,t)
    res=con.execute(m._transform_sql(sid)).fetch_arrow_table()
    return t,res
t,res=run("cbe-banking-survey--net-balancing-item")
print("net-balancing: RAW",len(t),"-> TRANSFORM",len(res))
print("dtypes",[(f.name,str(f.type)) for f in res.schema])
for r in res.slice(0,2).to_pylist(): print(r)
t2,r2=run("cbe-gdp--gdp-at-factor-cost-constant", fetch=True)
print("\nGDP factor cost: RAW",len(t2),"-> TRANSFORM",len(r2),
      "dims",dict(collections.Counter(r2.column("dimension").to_pylist())))
