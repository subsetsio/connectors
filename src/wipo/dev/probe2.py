import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get
API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}
def g(path):
    sep = "&" if "?" in path else "?"
    r = get(f"{API}/{path}{sep}lang=en", headers=H, timeout=(10,120)); r.raise_for_status(); return r

# ipschart for patent ind 10 rt 11
for ep in ["ipschart","chart-options"]:
    try:
        d = g(f"ips-search/{ep}?selectedTab=patent&indicator=10&reportType=11&fromYear=2022&toYear=2022").json()
        print(f"=== {ep} type={type(d).__name__}")
        s = json.dumps(d)
        print(s[:900])
    except Exception as e:
        print(f"=== {ep} ERR {e}")
    print()

# downloadCsv raw bytes for the SAME query, see exact cell formatting
r = g("ips-search/downloadCsv?selectedTab=patent&indicator=10&reportType=11&fromYear=2022&toYear=2022")
print("=== CSV ===")
print(r.text[:1200])
