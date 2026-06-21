import json, time
from concurrent.futures import ThreadPoolExecutor
from subsets_utils import get
BASE="https://trade-analytics.commerce.gov.in"
def supply(cc,year,flow):
    u=f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype={flow}&calyear={year}&hscode=HS2&commocode=HS&countryCode={cc}&region=COUNTRY&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD"
    d=get(u,timeout=(10,90)).json()
    return d.get('label',[]),d.get('value',[])
# year coverage for USA
for y in [2016,2017,2018,2024,2025,2026]:
    lab,val=supply("USA",y,"Export")
    print(f"USA Export {y}: n={len(lab)} ", (lab[0]['label'][:20], val[0]['value'][:10]) if lab else "")
# alignment check: label '85: ELEC...' with its value
lab,val=supply("USA",2025,"Export")
print("\nalignment USA 2025 Export:")
for i in range(3): print("  ",lab[i]['label'][:25],"=>",val[i]['value'])
# threaded test: 24 calls
jobs=[("USA",y,f) for y in [2023,2024,2025] for f in ["Export","Import"] for _ in range(4)]
t=time.time()
with ThreadPoolExecutor(max_workers=8) as ex:
    res=list(ex.map(lambda a: len(supply(*a)[0]), jobs))
print(f"\nthreaded {len(jobs)} calls in {time.time()-t:.1f}s, all98={all(r==98 for r in res)}")
