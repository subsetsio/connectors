import io, httpx, pandas as pd
from subsets_utils import get
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from subsets_utils import is_transient

def _net(e): return is_transient(e) or isinstance(e,(httpx.TransportError,))
@retry(retry=retry_if_exception(_net), stop=stop_after_attempt(6),
       wait=wait_exponential(multiplier=2,min=2,max=60), reraise=True)
def dl(url):
    r=get(url,timeout=(15,180)); r.raise_for_status(); return r.content

BASE="https://data.gov.au/data/api/3/action"
TAB={"csv","tsv","xls","xlsx","xlsm","xlsb"}
def is_tab(f):
    f=(f or "").lower().strip()
    return f in TAB or "excel" in f or "csv" in f or f.endswith(".xlsx") or f.endswith(".csv")

for pkg in ["pb_agcomd9abcc20141209_11a","agricultural-commodity-statistics-2017","pb_afastats13d9abmd20141121_11a","pb_avfesd9absf20141114","pe_alumc9aal20161017"]:
    r=dl(f"{BASE}/package_show?id={pkg}")
    import json; res=json.loads(r)["result"]["resources"]
    tabs=[x for x in res if is_tab(x.get("format"))]
    print(f"\n=== {pkg}: {len(tabs)} tabular ===")
    cells=0
    for x in tabs[:3]:
        c=dl(x["url"]); fmt=(x.get("format") or "").lower(); u=x["url"].lower()
        try:
            if "csv" in fmt or u.endswith(".csv") or u.endswith(".tsv"):
                df=pd.read_csv(io.BytesIO(c),dtype=str,header=None)
                sh={"_csv":df}
            else:
                sh=pd.read_excel(io.BytesIO(c),sheet_name=None,header=None,dtype=str)
            n=sum(int(d.notna().sum().sum()) for d in sh.values())
            cells+=n
            print(f"  {x.get('format'):24s} sheets={len(sh)} cells={n}")
        except Exception as e:
            print(f"  {x.get('format'):24s} PARSEFAIL {type(e).__name__}: {str(e)[:80]}")
    print("  total cells (first 3 res):", cells)
