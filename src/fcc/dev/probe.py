import json
from subsets_utils import get

# A spread of entity types: consumer complaints (live), a broadband Area Table,
# a Provider Table, EAS grantee, ULS locations (54 cols).
ids = ["3xyp-aqkj", "ymd4-xaiz", "2ra3-4jd4", "3b3k-34jp", "euz5-46g2"]
for rid in ids:
    # count
    c = get(f"https://opendata.fcc.gov/resource/{rid}.json",
            params={"$select": "count(*)"}, timeout=(10,120))
    cnt = c.json()
    # one row
    r = get(f"https://opendata.fcc.gov/resource/{rid}.json",
            params={"$limit": 2, "$order": ":id"}, timeout=(10,120))
    rows = r.json()
    keys = sorted(rows[0].keys()) if rows else []
    sys_keys = [k for k in keys if k.startswith(":")]
    print("====", rid, "count=", cnt)
    print("  ncols", len(keys))
    print("  sys/computed keys:", sys_keys)
    if rows:
        print("  sample row 0:", json.dumps(rows[0])[:600])
