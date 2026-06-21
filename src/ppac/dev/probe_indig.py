import json, re
from subsets_utils import post
def strip(s): return re.sub(r'<[^>]+>','',str(s)).strip()
for meth in ("getProduction","getProductionJson"):
    r=post(f"https://ppac.gov.in/AjaxController/{meth}",
           data={"financialYear":"2025-2026","reportBy":"1","pageId":"3"},
           headers={"X-Requested-With":"XMLHttpRequest"})
    j=json.loads(r.text); res=j["result"]
    rows=list(res.values()) if isinstance(res,dict) else res
    print(f"\n### {meth}: {len(rows)} rows; row0 keys={list(rows[0].keys())}")
    for row in rows[:6]:
        print("   ", {k:(strip(v) if isinstance(v,str) else v) for k,v in list(row.items())[:9]})
