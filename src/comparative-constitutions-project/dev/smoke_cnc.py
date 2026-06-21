import duckdb
import nodes.comparative_constitutions_project as m
from subsets_utils import load_raw_parquet

m.fetch_bulk_csv("comparative-constitutions-project-ccp-cnc")
t = load_raw_parquet("comparative-constitutions-project-ccp-cnc")
print("CNC raw rows/cols:", t.num_rows, len(t.column_names))
print("first cols:", t.column_names[:5])
con = duckdb.connect()
con.register("comparative-constitutions-project-ccp-cnc", t)
sql = [s for s in m.TRANSFORM_SPECS if s.id.endswith("ccp-cnc-transform")][0].sql
res = con.execute(sql).to_arrow_table()
print("CNC transform rows/cols:", res.num_rows, len(res.column_names))
print("year type:", res.schema.field("year").type, "| cowcode type:", res.schema.field("cowcode").type)
yr = con.execute('SELECT min(year), max(year), count(distinct year) FROM res').fetchone() if False else None
print("year range:", con.execute("SELECT min(TRY_CAST(year AS INT)), max(TRY_CAST(year AS INT)) FROM res").fetchone() if False else "n/a")
