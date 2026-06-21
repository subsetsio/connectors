import re, json
from subsets_utils import get
BASE = "https://trade-analytics.commerce.gov.in"
def J(tag,url):
    r=get(url,timeout=(10,90)); print(f"\n=== {tag} [{r.status_code}] len={len(r.text)}")
    try: d=r.json(); print(json.dumps(d)[:600] if not isinstance(d,list) else f"list len={len(d)} :: "+json.dumps(d)[:600])
    except Exception as e: print("non-json", r.text[:200])
    return r

# Is there a WORLD/All-countries option in the country dropdown?
html=get(f"{BASE}/public/country",timeout=(10,90)).text
opts=re.findall(r'<option[^>]*value="([A-Za-z0-9]+)"[^>]*>([^<]+)</option>', html)
worldish=[(c,n.strip()) for c,n in opts if re.search(r'world|all|total', n, re.I)]
print("WORLDISH OPTIONS:", worldish[:10])

# state import 2025
J("stateWise Import 2025", f"{BASE}/public/indiaTrade/getStateWiseTableData?year=2025&type=Import&currency=USD")

# supply data full value array (per-country) - check length & values
r=J("supply USA HS2 export FULL", f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype=Export&calyear=2025&hscode=HS2&commocode=HS&countryCode=USA&region=COUNTRY&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD")
d=r.json(); 
print("supply keys:", list(d.keys()), "label_count:", len(d.get('label',[])), "value_count:", len(d.get('value',[])) if isinstance(d.get('value'),list) else type(d.get('value')))
print("first value items:", json.dumps(d.get('value',[])[:3]), "supplyDemand sample:", json.dumps(d.get('supplyDemandData'))[:200])

# productYearlyData with WORLD-ish country
for cc in ["WORLD","ALL","WLD"]:
    J(f"productYearly HS85 cc={cc}", f"{BASE}/public/country/productYearlyData?hscode=85&countryCode={cc}&type=Export&indi=yearly&year=2025&hsnCode=HS2&caltype=cal&region=WORLD&regionCode=&regionCodetd=&pcCodes=ALL&qeCodes=ALL&commoType=HS&currency=USD")
