import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
m = get("https://gamma-api.polymarket.com/markets",
        params={"limit":1,"volume_num_min":1000000,"order":"volumeNum","ascending":"false"},
        timeout=(10,60)).json()[0]
tok = json.loads(m["clobTokenIds"])[0]
now=int(time.time())
for days in [200, 365, 500, 730, 1000]:
    r=get("https://clob.polymarket.com/prices-history",
          params={"market":tok,"startTs":now-days*86400,"endTs":now,"fidelity":1440},timeout=(10,90))
    h=r.json().get("history",[]) if r.status_code==200 else []
    print(f"{days}d window fid1440: status {r.status_code} pts {len(h)}")
