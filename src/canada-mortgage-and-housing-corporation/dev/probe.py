import json
from subsets_utils import get

BASE = "https://open.canada.ca/data/api/3/action"
# a few representative entity ids from the union
ids = [
    "38c6eca0-89d5-4f12-8ca1-3389e1f2755f",  # P1M Housing starts all areas SAAR (flagship)
    "a1361030-c554-4bf1-83fb-42392c03e1da",  # P1M Housing starts all areas Canada provinces
    "ae607e9a-2fce-4ed9-83e3-ba4cdbc24b8d",  # P1M mortgage lending rate
    "1146388b-a150-4e70-98ec-eb40cb9083c8",  # P1Y average rents
]
for pid in ids:
    r = get(f"{BASE}/package_show", params={"id": pid}, timeout=(10,60))
    rec = r.json()["result"]
    print("="*80)
    print(pid, "|", rec["title"])
    for res in rec["resources"]:
        print("   ", repr(res.get("format")), "| lang=", res.get("language"), "|", res.get("name"), "|", res.get("url"))
