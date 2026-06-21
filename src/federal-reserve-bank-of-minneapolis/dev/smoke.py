import duckdb
import nodes.federal_reserve_bank_of_minneapolis as M
from subsets_utils import load_raw_parquet

# 1) CPI scrape (small)
M.fetch_cpi("federal-reserve-bank-of-minneapolis-cpi-historical")
t = load_raw_parquet("federal-reserve-bank-of-minneapolis-cpi-historical")
print("CPI raw rows:", t.num_rows, "cols:", t.column_names)

# 2) prop-share IDDA module (31MB, exercises duckdb union + streaming writer)
M.fetch_idda_module("federal-reserve-bank-of-minneapolis-prop-share")
p = load_raw_parquet("federal-reserve-bank-of-minneapolis-prop-share")
print("prop-share raw rows:", p.num_rows, "cols:", p.column_names[:6], "...")

# 3) run the transform SQL for each over the raw parquet
con = duckdb.connect()
con.register("federal-reserve-bank-of-minneapolis-cpi-historical", t)
cpi_sql = [s.sql for s in M.TRANSFORM_SPECS if s.id.endswith("cpi-historical-transform")][0]
r = con.execute(cpi_sql).fetch_arrow_table()
print("CPI transform rows:", r.num_rows, "cols:", r.column_names)
print(con.execute(cpi_sql + " ").df().head(2).to_string())
print(con.execute(f"SELECT series, min(year), max(year), count(*) FROM ({cpi_sql}) GROUP BY series").df().to_string())

con.register("federal-reserve-bank-of-minneapolis-prop-share", p)
ps_sql = [s.sql for s in M.TRANSFORM_SPECS if s.id.endswith("prop-share-transform")][0]
r2 = con.execute(ps_sql).fetch_arrow_table()
print("prop-share transform rows:", r2.num_rows, "year type:", r2.schema.field("year").type)
print(con.execute(f"SELECT geo_var, count(*) FROM ({ps_sql}) GROUP BY geo_var").df().to_string())
