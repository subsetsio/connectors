import json
from subsets_utils import post
CASES = [
 ("getConsumptionPetroleumProductsData",43,"1","2025-2026"),
 ("getPetroleumProductData",42,"1","2025-2026"),
 ("getInternationalPricesCrudeOil",30,"4","2025-2026"),
 ("getProduction",3,"1","2025-2026"),
 ("getProductionJson",3,"1","2025-2026"),
 ("getImportExports",14,"1","2025-2026"),
 ("getImportExportsJson",14,"1","2025-2026"),
 ("getGasProduction",170,"4","2025-2026"),
 ("getGasConsumption",138,"4","2025-2026"),
 ("getCrudeProcessingData",41,"1","2025-2026"),
]
for meth,pid,rb,fy in CASES:
    try:
        r=post(f"https://ppac.gov.in/AjaxController/{meth}",
               data={"financialYear":fy,"reportBy":rb,"pageId":str(pid)},
               headers={"X-Requested-With":"XMLHttpRequest"})
        body=r.text.strip()
        try: j=json.loads(body)
        except Exception: print(f"\n### {meth} pid={pid}: NON-JSON, len={len(body)}: {body[:150]}"); continue
        res=j.get("result")
        if isinstance(res,dict):
            keys=list(res.keys())
            first=res[keys[0]] if keys else {}
            print(f"\n### {meth} pid={pid} rb={rb}: dict result, {len(keys)} rows. row0 keys={list(first.keys())}")
            print("   row0:", {k:first.get(k) for k in list(first.keys())[:10]})
        else:
            print(f"\n### {meth} pid={pid} rb={rb}: result type={type(res).__name__} val={str(res)[:120]} topkeys={list(j.keys())}")
    except Exception as e:
        print(f"\n### {meth} pid={pid}: ERR {type(e).__name__} {e}")
