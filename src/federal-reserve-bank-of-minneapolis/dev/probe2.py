import io, tempfile, os
import duckdb
import pandas as pd
from subsets_utils import get

BASE = "https://www.minneapolisfed.org/-/media/assets/institute/census/data-center"

# --- Test DuckDB union_by_name on pctl_of_inc (all=32 cols, na=24 cols) ---
paths = []
for variant in ("pctl_of_inc_all_data", "na_pctl_of_inc_all_data"):
    r = get(f"{BASE}/{variant}.csv", timeout=(10.0, 180.0)); r.raise_for_status()
    fd, p = tempfile.mkstemp(suffix=".csv"); os.write(fd, r.content); os.close(fd)
    paths.append(p)
con = duckdb.connect()
globlist = ", ".join(f"'{p}'" for p in paths)
t = con.execute(f"SELECT * FROM read_csv([{globlist}], union_by_name=true, sample_size=-1)").arrow()
print("pctl_of_inc unioned rows:", t.num_rows, "cols:", t.num_columns)
print("schema:")
for f in t.schema:
    print("   ", f.name, f.type)
# check na rows got nulls for top-tail
df = con.execute(f"SELECT geo_var, count(*) n, count(pctl99_999) nn FROM read_csv([{globlist}], union_by_name=true, sample_size=-1) GROUP BY geo_var ORDER BY 1").df()
print(df)
for p in paths: os.unlink(p)

# --- Test CPI HTML parse ---
print("\n=== CPI 1800 ===")
r = get("https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-", timeout=(10.0,60.0)); r.raise_for_status()
tables = pd.read_html(io.StringIO(r.text))
print("num tables:", len(tables))
for i, tb in enumerate(tables):
    print(i, tb.shape, list(tb.columns)[:5])
big = max(tables, key=lambda x: x.shape[0])
print("biggest head:")
print(big.head(3).to_string())
print("biggest tail:")
print(big.tail(3).to_string())
