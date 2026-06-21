import json
from subsets_utils import get, configure_http

def try_get(label, url, headers=None):
    try:
        r = get(url, headers=headers, timeout=(10.0, 60.0))
        print(f"[{label}] HTTP {r.status_code} len={len(r.content)}")
        return r
    except Exception as e:
        print(f"[{label}] ERROR {type(e).__name__}: {e}")
        return None

# 1) default UA — does subsets_utils default UA get blocked?
try_get("default-UA stocks", "https://api.nasdaq.com/api/screener/stocks?limit=2&offset=0")

# 2) browser UA via headers kwarg
BUA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
H = {"User-Agent": BUA, "Accept": "application/json"}
r = try_get("browser-UA stocks", "https://api.nasdaq.com/api/screener/stocks?limit=2&offset=0", headers=H)
if r and r.status_code == 200:
    d = r.json()["data"]
    print("  stocks headers:", list(d["table"]["headers"].keys()))
    print("  stocks totalrecords:", d["totalrecords"])
    print("  sample row:", json.dumps(d["table"]["rows"][0]))

r = try_get("hist AAPL", "https://api.nasdaq.com/api/quote/AAPL/historical?assetclass=stocks&fromdate=2021-01-01&todate=2026-06-18&limit=99999", headers=H)
if r and r.status_code == 200:
    d = r.json()["data"]
    tt = d.get("tradesTable") or {}
    print("  hist totalRecords:", d.get("totalRecords"), "rows:", len(tt.get("rows", [])))
    print("  hist headers:", list(tt.get("headers", {}).keys()))
    print("  hist sample:", json.dumps(tt.get("rows", [{}])[0]))

# 404 / bad symbol semantics
r = try_get("hist BADXYZ", "https://api.nasdaq.com/api/quote/ZZZZNOPE/historical?assetclass=stocks&fromdate=2021-01-01&todate=2026-06-18&limit=10", headers=H)
if r is not None:
    try:
        print("  bad body head:", json.dumps(r.json())[:300])
    except Exception as e:
        print("  bad not-json:", r.text[:200])
