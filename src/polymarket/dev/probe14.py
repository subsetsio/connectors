import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import datetime as dt

m = get("https://gamma-api.polymarket.com/markets",
        params={"limit":1,"volume_num_min":1000000,"order":"volumeNum","ascending":"false"},
        timeout=(10,60)).json()[0]
tok = json.loads(m["clobTokenIds"])[0]
now = int(time.time())

# debug 400 body for a 10-day past window
start = now - 10*86400; end = now
r = get("https://clob.polymarket.com/prices-history",
        params={"market":tok,"startTs":start,"endTs":end,"fidelity":60}, timeout=(10,90))
print("10d startTs/endTs:", r.status_code, r.text[:200])

# maybe params are startTs/endTs vs start/end (seconds vs ms)
for p in [{"startTs":start,"endTs":end},{"start":start,"end":end}]:
    pp=dict(p); pp.update({"market":tok,"fidelity":60})
    r=get("https://clob.polymarket.com/prices-history",params=pp,timeout=(10,90))
    print(p, "->", r.status_code, (r.text[:80] if r.status_code!=200 else f"points {len(r.json().get('history',[]))}"))

# fidelity variants with interval
for fid in [1,10,60,1440]:
    r=get("https://clob.polymarket.com/prices-history",params={"market":tok,"interval":"max","fidelity":fid},timeout=(10,90))
    h=r.json().get("history",[]) if r.status_code==200 else []
    print(f"interval=max fid={fid}: pts {len(h)} span_days {round((h[-1]['t']-h[0]['t'])/86400) if h else 0}")
