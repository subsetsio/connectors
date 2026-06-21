import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

# get a high-volume market token + created date
m = get("https://gamma-api.polymarket.com/markets",
        params={"limit":1,"volume_num_min":1000000,"order":"volumeNum","ascending":"false"},
        timeout=(10,60)).json()[0]
tok = json.loads(m["clobTokenIds"])[0]
print("market:", m["question"][:50], "created:", m["createdAt"], "closed:", m.get("closed"))

import datetime as dt
start = int(dt.datetime.fromisoformat(m["createdAt"].replace("Z","+00:00")).timestamp())
end = int(time.time())
print(f"span days: {(end-start)/86400:.0f}")

# Try whole range in one request at fidelity 60
for fid in [60]:
    r = get("https://clob.polymarket.com/prices-history",
            params={"market":tok,"startTs":start,"endTs":end,"fidelity":fid}, timeout=(10,90))
    h = r.json().get("history",[])
    print(f"fidelity={fid}: status {r.status_code}, points={len(h)}, "
          f"first_t={h[0]['t'] if h else None}, last_t={h[-1]['t'] if h else None}")
    if h:
        span = (h[-1]['t']-h[0]['t'])/86400
        print(f"   covered span: {span:.0f} days  -> {'FULL' if span > (end-start)/86400*0.9 else 'TRUNCATED'}")
