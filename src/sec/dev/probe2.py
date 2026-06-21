from subsets_utils import get, configure_http

# default UA
r = get("https://www.sec.gov/files/company_tickers.json", timeout=(10,60))
print("default UA company_tickers ->", r.status_code)

# configured UA
configure_http(headers={"User-Agent": "subsets.io connector nathan@subsets.io"})
r = get("https://www.sec.gov/files/company_tickers.json", timeout=(10,60))
print("configured UA company_tickers ->", r.status_code)
if r.status_code == 200:
    d = r.json()
    print("  n:", len(d), "sample:", d["0"])

r = get("https://www.sec.gov/files/company_tickers_exchange.json", timeout=(10,60))
print("configured UA tickers_exchange ->", r.status_code)
if r.status_code == 200:
    d = r.json()
    print("  fields:", d["fields"], "n:", len(d["data"]), "sample:", d["data"][0])
