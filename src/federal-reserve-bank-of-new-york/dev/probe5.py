import datetime
from subsets_utils import get
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
today=datetime.date.today()
def test(s,e):
    u=f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate={s}&endDate={e}"
    r=get(u,headers=UA,timeout=(10,180))
    body=r.text[:200]
    n=None
    try: n=len(r.json()["seclending"]["operations"])
    except: n=None
    print(f"{s}..{e}", r.status_code, "n=",n, "body=",repr(body) if r.status_code!=200 else "")
test("2024-01-01","2024-12-31")
test("2024-01-01",today.isoformat())
test("2022-01-01",today.isoformat())
test("2021-06-01",today.isoformat())
test((today-datetime.timedelta(days=730)).isoformat(), today.isoformat())
test((today-datetime.timedelta(days=366)).isoformat(), today.isoformat())
