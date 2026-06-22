import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import json

IDS = {
  "8zbs-9atu": "CES NSA 1990-current",
  "h44w-mqs3": "CES current",
  "tids-7w95": "OES occ wages",
  "nfe2-aprv": "LAUS substate",
  "7zu6-8dcr": "QCEW by NAICS & town",
}
for did, name in IDS.items():
    # count
    r = get(f"https://data.ct.gov/resource/{did}.json", params={"$select":"count(*)"}, timeout=(10,120))
    cnt = r.json()
    # sample
    r2 = get(f"https://data.ct.gov/resource/{did}.json", params={"$limit":"2"}, timeout=(10,120))
    rows = r2.json()
    print("="*70)
    print(did, "|", name, "| count:", cnt)
    if rows:
        print("columns:", list(rows[0].keys()))
        print("sample row 0:", json.dumps(rows[0], indent=None)[:600])
