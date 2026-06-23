import datetime
from subsets_utils import get
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
today=datetime.date.today().isoformat()
def f(u):
    r=get(u,headers=UA,timeout=(10,180)); return r
for s in ["2000-01-01","2008-01-01","2010-01-01","2015-01-01","2020-01-01"]:
    u=f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate={s}&endDate={today}"
    r=f(u)
    txt=r.text
    n=None
    try:
        d=r.json(); n=len(d["seclending"]["operations"])
    except Exception as e:
        n=f"ERR {txt[:150]}"
    print(s, r.status_code, n)
# also check seclending latest to find earliest available
r=f("https://markets.newyorkfed.org/api/seclending/all/results/summary/last/100000.json")
print("last-huge", r.status_code, r.text[:160])
