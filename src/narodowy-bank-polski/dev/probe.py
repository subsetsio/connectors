import json
from subsets_utils import get

def show(url):
    r = get(url, timeout=(10,60))
    print("URL", url, "->", r.status_code)
    if r.status_code == 200:
        d = r.json()
        print(json.dumps(d, ensure_ascii=False)[:600])
    print("---")

# table A date window
show("https://api.nbp.pl/api/exchangerates/tables/A/2024-01-02/2024-01-10/?format=json")
# table C date window
show("https://api.nbp.pl/api/exchangerates/tables/C/2024-01-02/2024-01-05/?format=json")
# gold date window
show("https://api.nbp.pl/api/cenyzlota/2024-01-02/2024-01-05/?format=json")
# 404 for a weekend
show("https://api.nbp.pl/api/exchangerates/tables/A/2024-01-06/2024-01-06/?format=json")
# over-93-day window -> 400
show("https://api.nbp.pl/api/exchangerates/tables/A/2024-01-01/2024-06-01/?format=json")
