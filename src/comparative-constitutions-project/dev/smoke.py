# Exercise fetch + transform mechanics locally for the two cheap nodes.
import duckdb
import nodes.comparative_constitutions_project as m
from subsets_utils import load_raw_parquet, load_raw_ndjson

# --- CCE bulk csv ---
m.fetch_bulk_csv("comparative-constitutions-project-ccp-cce")
t = load_raw_parquet("comparative-constitutions-project-ccp-cce")
print("CCE raw rows/cols:", t.num_rows, len(t.column_names), t.column_names)

# --- constitutions ---
m.fetch_constitutions("comparative-constitutions-project-constitutions")
rows = load_raw_ndjson("comparative-constitutions-project-constitutions")
print("constitutions rows:", len(rows))

# --- run the CCE transform SQL exactly as runtime would (view over raw arrow) ---
con = duckdb.connect()
cce = t  # arrow table
con.register("comparative-constitutions-project-ccp-cce", cce)
sql = [s for s in m.TRANSFORM_SPECS if s.id.endswith("ccp-cce-transform")][0].sql
res = con.execute(sql).fetch_arrow_table()
print("CCE transform rows:", res.num_rows)
print("CCE transform year/cowcode types:",
      res.schema.field("year").type, res.schema.field("cowcode").type)
