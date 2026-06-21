import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json

print("=== Socrata Synar escb-scz6: 2 rows ===")
r = get("https://data.cdc.gov/resource/escb-scz6.json", params={"$limit": 2}, timeout=(10,120))
rows = r.json()
print("status", r.status_code, "n", len(rows))
print(json.dumps(rows[0], indent=2))
print("keys:", list(rows[0].keys()))

print("\n=== Socrata count ===")
r = get("https://data.cdc.gov/resource/escb-scz6.json", params={"$select":"count(*)"}, timeout=(10,120))
print(r.json())

print("\n=== FindTreatment one state (id=5), page 1 pageSize 3 ===")
r = get("https://findtreatment.gov/locator/exportsAsJson/v2",
        params={"sAddr":'"39.5,-98.35"',"limitType":0,"limitValue":5,"sType":"both","pageSize":3,"page":1},
        timeout=(10,120))
d = r.json()
print("status", r.status_code, "recordCount", d.get("recordCount"), "totalPages", d.get("totalPages"), "page", d.get("page"))
print("row keys:", list(d["rows"][0].keys()))
print(json.dumps(d["rows"][0], indent=2)[:1500])
