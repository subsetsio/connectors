import sys, duckdb, pyarrow as pa
sys.path.insert(0,"src")
import nodes.india_commerce as m

countries={"USA":"United States","CHN":"China","DEU":"Germany"}
latest=2025; years=[2024,2025]

crows=[]
for c,n in countries.items(): crows+=m._bilateral_rows(c,n,latest)
ct=pa.Table.from_pylist(crows,schema=m.COUNTRY_SCHEMA)

mrows=[]
for c in countries:
  for y in years:
    for f in ("Export","Import"): mrows+=m._supply_rows(c,y,f)
mt=pa.Table.from_pylist(mrows,schema=m.COMMODITY_SCHEMA)

srows=[]
for y in years: srows+=m._state_rows(y)
st=pa.Table.from_pylist(srows,schema=m.STATE_SCHEMA)

print("raw rows: country",len(ct),"commodity",len(mrows),"state",len(st))

con=duckdb.connect()
con.register("india-commerce-country-trade",ct)
con.register("india-commerce-commodity-trade",mt)
con.register("india-commerce-state-trade",st)
for spec in m.TRANSFORM_SPECS:
    r=con.execute(spec.sql).fetch_arrow_table()
    print(f"\n## {spec.id}: {len(r)} rows; cols={r.column_names}")
    print(r.slice(0,4).to_pandas().to_string())
