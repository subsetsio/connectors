import re,json
from subsets_utils import get
BASE="https://trade-analytics.commerce.gov.in"
# region options in country page
html=get(f"{BASE}/public/country",timeout=(10,90)).text
# look for region select
for m in re.finditer(r'<select[^>]*id="([^"]*[Rr]egion[^"]*)"[^>]*>(.*?)</select>', html, re.S):
    print("SELECT id=",m.group(1))
    for o in re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]+)</option>', m.group(2))[:30]:
        print("   ",o)
# also any data-region attributes / region list endpoint
J=lambda t,u:(lambda r:print(f"[{r.status_code}] {t}:",json.dumps(r.json())[:300]))(get(u,timeout=(10,90)))
for ep in ["api/region","public/country/regionList","api/allRegion","public/getRegion"]:
    try: J(ep, f"{BASE}/{ep}")
    except Exception as e: print("ERR",ep,e)
# test supply with region aggregate guesses
for reg,rc in [("REGION","1"),("REGION","2"),("ASEAN",""),("REGION","EU")]:
    u=f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype=Export&calyear=2024&hscode=HS2&commocode=HS&countryCode=&region={reg}&regionCode={rc}&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD"
    try:
        d=get(u,timeout=(10,90)).json(); print(f"supply region={reg} rc={rc}: labels={len(d.get('label',[]))}")
    except Exception as e: print("ERR",reg,rc,e)
