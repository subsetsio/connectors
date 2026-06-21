import re, json
from subsets_utils import get

BASE = "https://trade-analytics.commerce.gov.in"

def show(tag, url):
    r = get(url, timeout=(10,90))
    print(f"\n=== {tag} [{r.status_code}] {url}")
    t = r.text
    print(t[:700])
    return r

# 1) country list from HTML
html = get(f"{BASE}/public/country", timeout=(10,90)).text
opts = re.findall(r'<option[^>]*value="([A-Z]{3})"[^>]*>([^<]+)</option>', html)
codes = [(c,n.strip()) for c,n in opts if c not in ("USD","INR")]
print("COUNTRY COUNT:", len(codes), "sample:", codes[:5], codes[-3:])

# 2) bilateral USA
show("bilateral USA", f"{BASE}/public/country/bilateralMonthlyDataPublic?indi=yearly&countryCode=USA&year=2025&region=COUNTRY&regionCode=&regionCodetd=&currency=USD")

# 3) state-wise table
show("stateWise Export", f"{BASE}/public/indiaTrade/getStateWiseTableData?year=2025&type=Export&currency=USD")
show("stateWise Import", f"{BASE}/public/indiaTrade/getStateWiseTableData?year=2024&type=Import&currency=USD")

# 4) commodity totals - try supply data variations
show("supply USA HS2 export", f"{BASE}/public/country/getIndiaSupplyDataPublic?impexptype=Export&calyear=2025&hscode=HS2&commocode=HS&countryCode=USA&region=COUNTRY&regionCode=&qeCodes=ALL&pcCodes=ALL&yeartype=cal&finyear=&currency=USD")
