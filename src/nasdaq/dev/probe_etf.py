from subsets_utils import get
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36","Accept":"application/json"}
def n(url):
    r=get(url,headers=H,timeout=(10,60)); r.raise_for_status(); d=r.json()["data"]["records"]
    return len(d["data"]["rows"]), d["totalrecords"], d.get("limit"), d.get("offset")
for lim in [50,100,500,5000]:
    print("etf limit",lim,"->",n(f"https://api.nasdaq.com/api/screener/etf?limit={lim}&offset=0"))
print("etf offset100 lim50 ->", n("https://api.nasdaq.com/api/screener/etf?limit=50&offset=100"))
print("etf download=true ->", n("https://api.nasdaq.com/api/screener/etf?download=true"))
# stocks for comparison
def ns(url):
    r=get(url,headers=H,timeout=(10,60)); r.raise_for_status(); d=r.json()["data"]
    return len(d["table"]["rows"]), d["totalrecords"]
print("stocks limit5000 ->", ns("https://api.nasdaq.com/api/screener/stocks?limit=5000&offset=0"))
print("stocks download=true ->", ns("https://api.nasdaq.com/api/screener/stocks?download=true"))
