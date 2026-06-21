from subsets_utils import get
r = get("https://api.nbp.pl/api/exchangerates/tables/C/2002-01-02/2002-01-31/", params={"format":"json"}, timeout=(10,120))
print(r.status_code)
if r.status_code==200:
    d=r.json()[0]
    print("keys:", list(d.keys()))
    print("rate0:", d["rates"][0])
