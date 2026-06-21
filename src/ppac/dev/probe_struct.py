import json, re
from subsets_utils import post
def strip(s): return re.sub(r'<[^>]+>','',str(s)).strip()
def show(meth,pid,rb,fy="2025-2026"):
    r=post(f"https://ppac.gov.in/AjaxController/{meth}",
           data={"financialYear":fy,"reportBy":rb,"pageId":str(pid)},
           headers={"X-Requested-With":"XMLHttpRequest"})
    j=json.loads(r.text)
    res=j["result"]
    rows = list(res.values()) if isinstance(res,dict) else res
    print(f"\n##### {meth} pid={pid}: {len(rows)} rows")
    for row in rows:
        t=strip(row.get("title",""))
        apr=row.get("april"); colspan=row.get("colspan")
        # classify
        nums=[row.get(m) for m in ("april","may","june") ]
        print(f"  cs={str(colspan):3s} apr={str(apr)[:14]:14s} | {t[:60]}")
show("getImportExports",14,"1")
show("getCrudeProcessingData",41,"1")
show("getGasProduction",170,"4")
