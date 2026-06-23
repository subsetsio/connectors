from subsets_utils import get
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
def yr(y):
    u=f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate={y}-01-01&endDate={y}-12-31"
    r=get(u,headers=UA,timeout=(10,120))
    try:
        ops=r.json()["seclending"]["operations"]
        print(y, r.status_code, "n=",len(ops))
    except: print(y, r.status_code, "ERR/none")
for y in [2006,2008,2009,2010,2013,2018,2020,2022,2024,2026]:
    yr(y)
