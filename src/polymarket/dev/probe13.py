import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import datetime as dt

m = get("https://gamma-api.polymarket.com/markets",
        params={"limit":1,"volume_num_min":1000000,"order":"volumeNum","ascending":"false"},
        timeout=(10,60)).json()[0]
tok = json.loads(m["clobTokenIds"])[0]
end = int(time.time())

for days in [400, 200, 120, 90, 60, 31]:
    start = end - days*86400
    r = get("https://clob.polymarket.com/prices-history",
            params={"market":tok,"startTs":start,"endTs":end,"fidelity":60}, timeout=(10,90))
    h = r.json().get("history",[]) if r.status_code==200 else []
    print(f"{days}d: status {r.status_code} points {len(h)}")

# also test 'interval' param shorthand which docs may support
print("\n== interval=max ==")
r = get("https://clob.polymarket.com/prices-history", params={"market":tok,"interval":"max","fidelity":60}, timeout=(10,90))
h=r.json().get("history",[]) if r.status_code==200 else []
print("status",r.status_code,"points",len(h), "span_days", round((h[-1]['t']-h[0]['t'])/86400) if h else 0)
