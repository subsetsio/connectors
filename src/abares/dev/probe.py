import io, json
from subsets_utils import get
import pandas as pd

BASE = "https://data.gov.au/data/api/3/action"
TAB = {"csv","tsv","xls","xlsx","xlsm","xlsb"}
def is_tab(f):
    f=(f or "").lower().strip()
    return f in TAB or "excel" in f or "csv" in f or f.endswith(".xlsx") or f.endswith(".csv")

def excel_engine(fmt, url):
    f=(fmt or "").lower(); u=url.lower()
    if "xls" in f and "xlsx" not in f and "2007" not in f and not u.endswith(("xlsx","xlsm")):
        if u.endswith(".xls"): return "xlrd"
    return None  # let pandas auto-detect

for pkg in ["forests-of-australia-2023","pb_agcomd9abcc20141209_11a","agricultural-commodity-statistics-2017","pb_aucrpd9aba_20141202_11a","australian-water-markets-report-2015-16"]:
    r = get(f"{BASE}/package_show", params={"id":pkg}, timeout=(10,120))
    r.raise_for_status()
    res = r.json()["result"]["resources"]
    tabs = [x for x in res if is_tab(x.get("format"))]
    print(f"\n=== {pkg}: {len(res)} resources, {len(tabs)} tabular ===")
    x = tabs[0]
    print("  fmt:", x.get("format"), "| url:", x.get("url")[:90])
    dl = get(x["url"], timeout=(10,180))
    dl.raise_for_status()
    content = dl.content
    print("  bytes:", len(content), "| ctype:", dl.headers.get("content-type"))
    fmt=(x.get("format") or "").lower()
    if "csv" in fmt or x["url"].lower().endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=5)
        print("  CSV cols:", list(df.columns)[:8])
    else:
        try:
            sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, nrows=8)
            print("  sheets:", list(sheets.keys())[:6])
            first=list(sheets.values())[0]
            print("  sheet0 shape:", first.shape, "| row0:", [str(c)[:20] for c in first.iloc[0].tolist()[:6]])
        except Exception as e:
            print("  EXCEL PARSE FAIL:", type(e).__name__, str(e)[:120])
