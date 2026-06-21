import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

# pick an OLD market (low volume_num_min, closed, old) to test full-history coverage
m = get("https://gamma-api.polymarket.com/markets",
        params={"limit":1,"volume_num_min":5000000,"order":"volumeNum","ascending":"false","closed":"true"},
        timeout=(10,60)).json()[0]
tok = json.loads(m["clobTokenIds"])[0]
print("market:", m["question"][:50], "created", m["createdAt"][:10], "closed", m.get("closed"), "endDate", m.get("endDate","")[:10])

import datetime as dt
for iv in ["1d","1w","1m","max"]:
    for fid in [60, 1440]:
        r=get("https://clob.polymarket.com/prices-history",
              params={"market":tok,"interval":iv,"fidelity":fid},timeout=(10,90))
        h=r.json().get("history",[]) if r.status_code==200 else []
        if h:
            span=(h[-1]['t']-h[0]['t'])/86400
            first=dt.datetime.utcfromtimestamp(h[0]['t']).date()
            last=dt.datetime.utcfromtimestamp(h[-1]['t']).date()
            print(f"interval={iv:4} fid={fid:4}: status {r.status_code} pts {len(h):4} span {span:.0f}d [{first}..{last}]")
        else:
            print(f"interval={iv:4} fid={fid:4}: status {r.status_code} pts 0")
