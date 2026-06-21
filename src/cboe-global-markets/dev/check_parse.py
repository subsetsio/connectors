import duckdb
import pyarrow as pa
from subsets_utils import get
from nodes.cboe_global_markets import _parse_history, SCHEMA

def fetch(sym):
    tok = sym.lstrip(".")
    r = get(f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{tok}_History.csv", timeout=(10.0,120.0))
    r.raise_for_status()
    return r.text

cols = {k: [] for k in ("symbol","date","open","high","low","close")}
for sym in ["VIX", "SPX", ".MSDXUTPU"]:
    c = _parse_history(sym, fetch(sym))
    for k in cols:
        cols[k].extend(c[k])
    print(sym, "rows", len(c["date"]), "sample", {k: c[k][0] for k in cols})

t = pa.table(cols, schema=SCHEMA)
print("table rows", len(t))
con = duckdb.connect()
con.register("v", t)
res = con.execute("""
    SELECT symbol, strptime(date,'%m/%d/%Y')::DATE AS date, open, high, low, close
    FROM v WHERE date IS NOT NULL AND close IS NOT NULL
""").arrow()
print("transformed rows", len(res))
print(res.slice(0,2).to_pylist())
print("max date", con.execute("SELECT max(strptime(date,'%m/%d/%Y')::DATE) FROM v").fetchone())
