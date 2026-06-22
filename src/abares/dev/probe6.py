import io, httpx, json, pandas as pd
from subsets_utils import get, is_transient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
def _net(e): return is_transient(e) or isinstance(e,(httpx.TransportError,))
@retry(retry=retry_if_exception(_net), stop=stop_after_attempt(8),
       wait=wait_exponential(multiplier=1,min=1,max=15), reraise=True)
def dl(url):
    r=get(url,timeout=(15,180)); r.raise_for_status(); return r.content
BASE="https://data.gov.au/data/api/3/action"
TAB={"csv","tsv","xls","xlsx","xlsm","xlsb"}
def is_tab(f):
    f=(f or "").lower().strip()
    return f in TAB or "excel" in f or "csv" in f or f.endswith(".xlsx") or f.endswith(".csv")
def parse(c, fmt, url):
    u=url.lower(); fmt=(fmt or "").lower()
    if "csv" in fmt or u.endswith(".csv"):
        return {"_data":pd.read_csv(io.BytesIO(c),dtype=str,header=None,on_bad_lines="skip",encoding_errors="replace")}
    if "tsv" in fmt or u.endswith(".tsv"):
        return {"_data":pd.read_csv(io.BytesIO(c),sep="\t",dtype=str,header=None,on_bad_lines="skip",encoding_errors="replace")}
    return pd.read_excel(io.BytesIO(c),sheet_name=None,header=None,dtype=str)
for pkg in ["pb_agcomd9abcc20141209_11a","pb_afastats13d9abmd20141121_11a","pb_avgfb9absf20170207"]:
    res=json.loads(dl(f"{BASE}/package_show?id={pkg}"))["result"]["resources"]
    tabs=[x for x in res if is_tab(x.get("format"))]
    print(f"=== {pkg}: {len(tabs)} tab res ===")
    for x in tabs:
        try:
            sh=parse(dl(x["url"]), x.get("format"), x["url"])
            n=sum(int(d.notna().sum().sum()) for d in sh.values())
            print(f"   OK {str(x.get('format')):22s} sheets={len(sh):2d} cells={n}")
        except Exception as e:
            print(f"   FAIL {str(x.get('format')):20s} {type(e).__name__}: {str(e)[:70]}")
