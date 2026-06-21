import sys, os, json, gzip, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import duckdb
from nodes.polymarket import _market_row, _event_row, TRANSFORM_SPECS, _yes_no_prices

# tiny samples
mk = get("https://gamma-api.polymarket.com/markets/keyset", params={"limit":20}, timeout=(10,60)).json()["markets"]
ev = get("https://gamma-api.polymarket.com/events/keyset", params={"limit":20}, timeout=(10,60)).json()["events"]
mrows=[_market_row(m) for m in mk if m.get("id")]
erows=[_event_row(e) for e in ev if e.get("id")]
ph=[{"market_id":"x","timestamp":1700000000,"price":0.5},{"market_id":"x","timestamp":1700000000,"price":0.5},{"market_id":"y","timestamp":1700086400,"price":0.9}]

d=tempfile.mkdtemp()
def w(name,rows):
    p=os.path.join(d,name+".ndjson")
    with open(p,"w") as f:
        for r in rows: f.write(json.dumps(r)+"\n")
    return p
paths={"polymarket-markets":w("m",mrows),"polymarket-events":w("e",erows),"polymarket-price-history":w("p",ph)}

con=duckdb.connect()
for dep,p in paths.items():
    con.execute(f'CREATE VIEW "{dep}" AS SELECT * FROM read_json_auto(\x27{p}\x27)')

import nodes.polymarket as N
for spec in TRANSFORM_SPECS:
    try:
        res=con.execute(spec.sql).fetchdf()
        print(f"OK {spec.id}: {len(res)} rows, cols={list(res.columns)[:6]}...")
    except Exception as ex:
        print(f"FAIL {spec.id}: {type(ex).__name__}: {ex}")
