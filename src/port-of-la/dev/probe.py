import json
from subsets_utils import get

# Probe a few entities to see SODA JSON shape + types
for eid in ["tsuv-4rgh", "38a8-tm7u", "jmt8-y5rm", "i9rh-q5gx"]:
    url = f"https://data.lacity.org/resource/{eid}.json"
    r = get(url, params={"$limit": 3, "$offset": 0}, timeout=(10.0, 60.0))
    r.raise_for_status()
    rows = r.json()
    print(f"=== {eid} :: {len(rows)} rows (showing first) ===")
    if rows:
        for k, v in rows[0].items():
            print(f"   {k!r}: {v!r}  ({type(v).__name__})")
    # total count
    rc = get(url, params={"$select": "count(*)"}, timeout=(10.0, 60.0))
    print("   count:", rc.json())
    print()
