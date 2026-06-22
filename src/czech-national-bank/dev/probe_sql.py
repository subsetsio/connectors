import sys, json, tempfile, duckdb
sys.path.insert(0, "src"); sys.path.insert(0, "src/nodes")
from subsets_utils import get
import czech_national_bank as m

checks = {
    "exrates-daily": ("exrates/daily-year", {"year":2023,"lang":"EN"}, "rates"),
    "fxrates-daily": ("fxrates/daily-year", {"year":2023,"lang":"EN"}, "rates"),
    "exrates-monthly-averages": ("exrates/monthly-averages-year", {"year":2023,"lang":"EN"}, "averages"),
    "exrates-quarterly-averages": ("exrates/quarterly-averages-year", {"year":2023,"lang":"EN"}, "averages"),
    "pribor-daily": ("pribor/daily-year", {"year":2023}, "pribs"),
    "czeonia-daily": ("czeonia/daily-year", {"year":2023}, "rates"),
    "omo-daily": ("omo/daily-year", {"year":2023}, "operations"),
}
con = duckdb.connect()

def load(dep, rows):
    jf = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False).name
    with open(jf, "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    con.execute(f'CREATE OR REPLACE TABLE "{dep}" AS SELECT * FROM read_json_auto(?)', [jf])

for eid,(path,params,wrap) in checks.items():
    rows = get(m.BASE+path, params=params, timeout=(10,120)).json()[wrap]
    dep = f"czech-national-bank-{eid}"
    load(dep, rows)
    res = con.execute(m._SQL_BY_ENTITY[eid].format(dep=dep)).arrow()
    print(f"{eid}: in={len(rows)} out={res.num_rows} cols={res.column_names}")

fwd = get(m.BASE+"forward/daily-range-currency-pair-maturity",
          params={"currencyPair":"EUR_TO_CZK","maturity":"THREE_MONTH","dateFrom":"2020-01-01","dateTo":"2023-12-31"},
          timeout=(10,120)).json()["forwardPoints"]
load("czech-national-bank-forward-daily", fwd)
res = con.execute(m._SQL_BY_ENTITY["forward-daily"].format(dep="czech-national-bank-forward-daily")).arrow()
print(f"forward-daily: in={len(fwd)} out={res.num_rows} cols={res.column_names}")
