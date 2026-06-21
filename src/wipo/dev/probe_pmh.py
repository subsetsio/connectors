import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}
HC = {"Accept-Language": "en"}


def g(path, headers=H):
    sep = "&" if "?" in path else "?"
    return get(f"{API}/{path}{sep}lang=en", headers=headers, timeout=(10, 120))


# selection list keys for pmh pct ind 1001
sel = g("pmh-search/loadOffOrgClassList?indicator=1001").json()
print("keys:", list(sel.keys()))
for k, v in sel.items():
    if isinstance(v, dict):
        print(f"  {k}: {len(v)} entries, first 3 codes:", list(v.keys())[:3])
    else:
        print(f"  {k}: {v!r}")

off_codes = list((sel.get("pmhOffList") or {}).keys())
ori_codes = list((sel.get("pmhOriginList") or {}).keys())
cls_codes = list((sel.get("pmhClassList") or {}).keys())
print("\noff", len(off_codes), "ori", len(ori_codes), "class", len(cls_codes))

# Try table-result with selection values (all offices, total origin)
params = {
    "selectedTab": "pct", "indicator": "1001", "reportType": "4001",
    "fromYear": "2020", "toYear": "2024", "lang": "en",
}
# Try ALL origins + each office
if ori_codes:
    params["pmhOriSelValues"] = ori_codes
if off_codes:
    params["pmhOffSelValues"] = off_codes
if cls_codes:
    params["pmhClassSelValues"] = cls_codes
r = get(f"{API}/pmh-search/table-result", params=params, headers=H, timeout=(10, 180))
print("\n=== table-result WITH sel values [", r.status_code, "]")
txt = r.text
print(txt[:600])
d = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
if isinstance(d, dict) and d.get("records"):
    print("nrecords:", len(d["records"]), "cols:", json.dumps(d.get("columns"))[:200])
    print("rec0:", json.dumps(d["records"][0]))

# downloadCsv with same params
r2 = get(f"{API}/pmh-search/downloadCsv", params=params, headers=HC, timeout=(10, 180))
print("\n=== downloadCsv WITH sel values [", r2.status_code, "] ctype", r2.headers.get("content-type"))
print(repr(r2.text[:800]))
