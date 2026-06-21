import json
from subsets_utils import get
H={"Accept":"application/json"}
def g(label,url):
    try:
        r=get(url,headers=H,timeout=(10.0,60.0)); 
        print(f"[{label}] {r.status_code}")
        return r.json()
    except Exception as e:
        print(f"[{label}] ERR {type(e).__name__}: {e}"); return None

d=g("etf-full","https://api.nasdaq.com/api/screener/etf?limit=5&offset=0")
if d: 
    recs=d["data"]["records"]; print("  etf total:",recs["totalrecords"],"keys row0:",list(recs["data"]["rows"][0].keys()))
d=g("etf-hist","https://api.nasdaq.com/api/quote/QQQ/historical?assetclass=etf&fromdate=2024-01-01&todate=2026-06-18&limit=99999")
if d: 
    tt=d["data"]["tradesTable"]; print("  qqq rows:",len(tt["rows"]),"sample:",json.dumps(tt["rows"][0]))
d=g("earn","https://api.nasdaq.com/api/calendar/earnings?date=2026-06-18")
if d: print("  earn rows:",len(d["data"].get("rows",[])),"hdrs:",list(d["data"].get("headers",{}).keys()))
d=g("ipo","https://api.nasdaq.com/api/ipo/calendar?date=2026-05")
if d: print("  ipo keys:",list(d["data"].keys()), "priced rows:", len(d["data"].get("priced",{}).get("rows",[])))
d=g("split","https://api.nasdaq.com/api/calendar/splits")
if d: print("  split rows:",len(d["data"].get("rows",[])),"hdrs:",list(d["data"].get("headers",{}).keys()))
d=g("div","https://api.nasdaq.com/api/calendar/dividends?date=2026-06-15")
if d: print("  div rows:",len(d["data"].get("calendar",{}).get("rows",[])),"hdrs:",list(d["data"].get("calendar",{}).get("headers",{}).keys()), "sample:", json.dumps(d["data"]["calendar"]["rows"][0]) if d["data"].get("calendar",{}).get("rows") else "none")
