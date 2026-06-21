import json
from subsets_utils import get

SID = "Q.5B0.5B0.C.5A.BKC.ASTT.1.ALL.MX.TO1.ALL"
url = f"https://api.worldbank.org/v2/sources/54/country/all/series/{SID}/time/all"
r = get(url, params={"format": "json", "per_page": 3, "page": 1}, timeout=(10, 120))
data = r.json()
print("ENVELOPE TYPE:", type(data))
print("TOP KEYS:", list(data.keys()) if isinstance(data, dict) else "list")
print(json.dumps(data, indent=2)[:2500])

# indicators list shape
r2 = get("https://api.worldbank.org/v2/sources/54/indicators",
         params={"format": "json", "per_page": 2, "page": 1}, timeout=(10, 120))
d2 = r2.json()
print("\nINDICATORS PAGEINFO:", json.dumps(d2[0], indent=2))
print("INDICATOR ROW0:", json.dumps(d2[1][0], indent=2))
