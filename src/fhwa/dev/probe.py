import json
from subsets_utils import get

IDS = {
    "54nx-se7f": "VMT-421C",
    "ix2d-bsqq": "SF-1",
    "hvfw-tcmn": "MF-202",
    "taz8-hut2": "FE-210",
    "mt5m-skz3": "Truck S&W",
}

for fxf, label in IDS.items():
    print("=" * 70)
    print(fxf, label)
    cnt = get(f"https://datahub.transportation.gov/resource/{fxf}.json",
              params={"$select": "count(*)"}, timeout=(10, 60)).json()
    print("count:", cnt)
    rows = get(f"https://datahub.transportation.gov/resource/{fxf}.json",
               params={"$limit": 3}, timeout=(10, 60)).json()
    for r in rows[:2]:
        print(json.dumps(r, indent=1))
