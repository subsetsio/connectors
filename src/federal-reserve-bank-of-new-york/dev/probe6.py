import datetime
from subsets_utils import get
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
def test(s,e):
    u=f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate={s}&endDate={e}"
    r=get(u,headers=UA,timeout=(10,180))
    n=None
    try: 
        ops=r.json()["seclending"]["operations"]; n=len(ops)
        dates=[o["operationDate"] for o in ops]
        print(f"{s}..{e}",r.status_code,"n=",n,"min=",min(dates),"max=",max(dates))
    except Exception as ex: print(f"{s}..{e}",r.status_code,"ERR")
# latest op?
r=get("https://markets.newyorkfed.org/api/seclending/all/results/summary/latest.json",headers=UA,timeout=(10,60))
print("latest:",r.status_code, r.text[:200])
test("2000-01-01","2024-12-31")
test("2008-01-01","2025-12-31")
test("2008-01-01","2026-06-23")
test("2025-01-01","2025-12-31")
