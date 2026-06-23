from subsets_utils import get
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
def yr(y):
    u=f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate={y}-01-01&endDate={y}-12-31"
    r=get(u,headers=UA,timeout=(10,120))
    try:
        ops=r.json()["seclending"]["operations"]; print(y, r.status_code, "n=",len(ops))
    except: print(y, r.status_code, "ERR", r.text[:80])
for y in [1990,1999,2000,2001,2003,2005]:
    yr(y)
