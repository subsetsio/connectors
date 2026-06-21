from subsets_utils import get
import json

def show(url):
    r = get(url, timeout=(10,60))
    print(url, "->", r.status_code)
    return r

# 1. company_tickers_exchange.json shape
r = show("https://www.sec.gov/files/company_tickers_exchange.json")
if r.status_code == 200:
    d = r.json()
    print("  fields:", d.get("fields"))
    print("  n rows:", len(d.get("data", [])))
    print("  sample:", d["data"][0])

# 2. frames: duration annual, quarterly, instant for Assets / Revenues
for url in [
    "https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2022.json",       # annual duration
    "https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2022Q1.json",     # quarterly duration
    "https://data.sec.gov/api/xbrl/frames/us-gaap/Assets/USD/CY2022Q1I.json",      # instant
    "https://data.sec.gov/api/xbrl/frames/us-gaap/Assets/USD/CY2022.json",         # annual on instant concept (expect 404?)
    "https://data.sec.gov/api/xbrl/frames/dei/EntityCommonStockSharesOutstanding/shares/CY2022Q1I.json",
    "https://data.sec.gov/api/xbrl/frames/us-gaap/EarningsPerShareBasic/USD-per-shares/CY2022.json",
    "https://data.sec.gov/api/xbrl/frames/us-gaap/DOESNOTEXISTxyz/USD/CY2022.json",  # bad tag -> 404
]:
    r = get(url, timeout=(10,60))
    print(url, "->", r.status_code, end="")
    if r.status_code == 200:
        d = r.json()
        print("  pts=%d keys=%s row0keys=%s" % (d.get("pts"), list(d.keys()), list(d["data"][0].keys()) if d["data"] else []))
        print("     label=%r" % d.get("label"))
        print("     row0=%s" % d["data"][0])
    else:
        print()
