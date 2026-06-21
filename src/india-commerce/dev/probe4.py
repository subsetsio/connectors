import json
from subsets_utils import get
BASE="https://trade-analytics.commerce.gov.in"
def J(tag,u):
    try:
        r=get(u,timeout=(10,90)); d=r.json()
        n=len(d) if isinstance(d,(list,dict)) else '?'
        if isinstance(d,dict): n=f"dict keys={list(d.keys())} labels={len(d.get('label',[]))} values={len(d.get('value',[]))}"
        print(f"[{r.status_code}] {tag}: {n}")
        s=json.dumps(d); print("   ",s[:240])
    except Exception as e:
        print(f"ERR {tag}: {type(e).__name__} {e}")

# supply with region=WORLD variants
J("supply region=WORLD cc=blank", f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype=Export&calyear=2024&hscode=HS2&commocode=HS&countryCode=&region=WORLD&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD")
J("supply region=WORLD cc=WRD", f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype=Export&calyear=2024&hscode=HS2&commocode=HS&countryCode=WRD&region=WORLD&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD")
# guess national commodity endpoints
for ep in ["indiaTrade/getCommodityWiseTableData","indiaTrade/getCommodityWisedata","commodity/getCommodityWiseTableData","country/getIndiaSupplyDataPublic"]:
    J(ep+" (Export 2024 HS2)", f"{BASE}/public/{ep}?impexptype=Export&type=Export&txtype=Export&calyear=2024&year=2024&hscode=HS2&hsnCode=HS2&commocode=HS&commoType=HS&countryCode=IND&region=COUNTRY&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD")
