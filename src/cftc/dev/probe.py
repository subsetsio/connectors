import json
from subsets_utils import get

RESOURCES = {
    "legacy_fo": "6dca-aqww",
    "legacy_comb": "jun7-fc8e",
    "disagg_fo": "72hh-3qpy",
    "disagg_comb": "kh3c-gbw2",
    "tff_fo": "gpe5-46if",
    "tff_comb": "yw9f-hn96",
    "cit": "4zgm-a668",
}

for name, rid in RESOURCES.items():
    url = f"https://publicreporting.cftc.gov/resource/{rid}.json"
    r = get(url, params={"$limit": 1}, timeout=(10.0, 60.0))
    r.raise_for_status()
    rows = r.json()
    keys = sorted(rows[0].keys()) if rows else []
    print(f"\n=== {name} ({rid})  fields={len(keys)} ===")
    print("has futonly_or_combined:", "futonly_or_combined" in keys)
    print(json.dumps(keys))
