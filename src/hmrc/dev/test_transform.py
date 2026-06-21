import duckdb, pyarrow as pa
from subsets_utils import get
import importlib.util, sys, pathlib

# import the node module to reuse its SCHEMAS and _SQL
spec = importlib.util.spec_from_file_location("hmrcnode", pathlib.Path(__file__).parents[1]/"src/nodes/hmrc.py")
m = importlib.util.module_from_spec(spec); sys.modules["hmrcnode"]=m; spec.loader.exec_module(m)

BASE="https://api.uktradeinfo.com"
def page(ent, **p):
    return get(f"{BASE}/{ent}", params=p, timeout=(10,120)).json()["value"]

# Build a small raw table per entity exactly as the fetch fn would, then run the
# published transform SQL against it via a DuckDB view named after the spec id.
cases = {
    "hmrc-ots": ("OTS", {"$filter":"MonthId eq 202401","$top":50}),
    "hmrc-rts": ("RTS", {"$filter":"MonthId eq 202401","$top":50}),
    "hmrc-trade": ("Trade", {"$filter":"MonthId eq 202401","$top":50}),
    "hmrc-import": ("Import", {"$filter":"MonthId eq 202401","$top":50}),
    "hmrc-export": ("Export", {"$filter":"MonthId eq 202401","$top":50}),
    "hmrc-yearlytrade": ("YearlyTrade", {"$filter":"Year eq 2024","$top":50}),
    "hmrc-commodity": ("Commodity", {"$top":50}),
}
con = duckdb.connect()
for sid,(ent,params) in cases.items():
    rows = page(ent, **params)
    tbl = pa.Table.from_pylist(rows, schema=m.SCHEMAS[ent])
    con.register("raw_tmp", tbl)
    con.execute(f'CREATE OR REPLACE TEMP VIEW "{sid}" AS SELECT * FROM raw_tmp')
    out = con.execute(m._SQL[sid]).arrow().read_all()
    print(f"\n== {sid}: in={len(tbl)} out={len(out)} cols={out.column_names}")
    print(out.slice(0,2).to_pylist())
    con.unregister("raw_tmp")
print("\nALL TRANSFORMS OK")
