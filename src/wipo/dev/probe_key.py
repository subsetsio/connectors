import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}


def g(path, headers=H):
    sep = "&" if "?" in path else "?"
    return get(f"{API}/{path}{sep}lang=en", headers=headers, timeout=(10, 120))


# key-search json variant
for ep in ["key-search/keysearch-json/201", "keyindicator/keysearch-json/201"]:
    r = g(ep)
    print(f"=== {ep} [{r.status_code}] ctype={r.headers.get('content-type')}")
    print(r.text[:900])
    print()

# A messy key indicator (top 20 offices) CSV layout
r = g("keyindicator/downloadCsv/221", headers={"Accept-Language": "en"})
print("=== downloadCsv/221 (top 20 offices) ===")
print(repr(r.text[:900]))
print()

# pmh monthly (reportType 4003) — what columns?
sel = g("pmh-search/loadOffOrgClassList?indicator=1001").json()
off = list((sel.get("pmhOffList") or {}).keys())
ori = list((sel.get("pmhOriginList") or {}).keys())
params = {"selectedTab": "pct", "indicator": "1001", "reportType": "4003",
          "fromYear": "2023", "toYear": "2024", "lang": "en",
          "pmhOffSelValues": off, "pmhOriSelValues": ori}
r = get(f"{API}/pmh-search/table-result", params=params, headers=H, timeout=(10, 180))
print("=== pmh MONTHLY table-result [", r.status_code, "]")
d = r.json()
print("columns:", json.dumps(d.get("columns"))[:500])
print("rec0:", json.dumps((d.get("records") or [None])[0])[:400])
