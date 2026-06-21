import io, duckdb, pandas as pd, pyarrow as pa
from subsets_utils import get
import sys
sys.path.insert(0, "src")
import nodes.geopolitical_risk_index as n

# Reuse parse logic by monkeypatching save_raw_parquet to capture tables.
captured = {}
def fake_save(table, asset):
    captured[asset] = table
n.save_raw_parquet = fake_save

n.fetch_monthly("geopolitical-risk-index-gpr-monthly")
n.fetch_country_monthly("geopolitical-risk-index-gpr-country-monthly")
n.fetch_daily("geopolitical-risk-index-gpr-daily")

con = duckdb.connect()
for spec in n.TRANSFORM_SPECS:
    dep = spec.deps[0]
    tbl = captured[dep]
    con.register(dep, tbl)
    res = con.execute(spec.sql).fetch_arrow_table()
    print(spec.id, "->", res.num_rows, "rows,", res.num_columns, "cols")
    print("   cols:", res.column_names[:12])
    con.unregister(dep)
