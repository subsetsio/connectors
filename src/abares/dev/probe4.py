import io, time, httpx, json, pandas as pd
from subsets_utils import get, configure_http, is_transient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

configure_http(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"})

def _net(e): return is_transient(e) or isinstance(e,(httpx.TransportError,))
@retry(retry=retry_if_exception(_net), stop=stop_after_attempt(6),
       wait=wait_exponential(multiplier=1,min=1,max=20), reraise=True)
def dl(url):
    r=get(url,timeout=(15,180)); r.raise_for_status(); return r.content

BASE="https://data.gov.au/data/api/3/action"
TAB={"csv","tsv","xls","xlsx","xlsm","xlsb"}
def is_tab(f):
    f=(f or "").lower().strip()
    return f in TAB or "excel" in f or "csv" in f or f.endswith(".xlsx") or f.endswith(".csv")
ok=0; fail=0
for pkg in ["pb_agcomd9abcc20141209_11a","agricultural-commodity-statistics-2017","pb_afastats13d9abmd20141121_11a","pb_avfesd9absf20141114","pe_alumc9aal20161017","pb_aucrpd9aba_20141202_11a"]:
    res=json.loads(dl(f"{BASE}/package_show?id={pkg}"))["result"]["resources"]
    tabs=[x for x in res if is_tab(x.get("format"))]
    cells=0
    for x in tabs[:2]:
        c=dl(x["url"]); fmt=(x.get("format") or "").lower(); u=x["url"].lower()
        try:
            if "csv" in fmt or u.endswith((".csv",".tsv")):
                sh={"_csv":pd.read_csv(io.BytesIO(c),dtype=str,header=None)}
            else:
                sh=pd.read_excel(io.BytesIO(c),sheet_name=None,header=None,dtype=str)
            cells+=sum(int(d.notna().sum().sum()) for d in sh.values()); ok+=1
        except Exception as e:
            print("  PARSEFAIL",pkg,x.get('format'),type(e).__name__,str(e)[:60]); fail+=1
    print(f"{pkg:45s} tabs={len(tabs)} cells(2res)={cells}")
print("OK",ok,"FAIL",fail)
