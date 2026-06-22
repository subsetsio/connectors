import json
from utils import install_ca, parse_census_excel
from subsets_utils import get
from constants import ENTITY_FILES
install_ca()
for eid, info in ENTITY_FILES.items():
    url = info["urls"][0]
    blob = get(url, timeout=(10,180)).content
    rows = parse_census_excel(blob, url)
    print(f"\n===== {eid} ({info['table_code']}/{info['census_year']}) members={len(info['urls'])} file0_rows={len(rows)} =====")
    if rows:
        print("  cols:", list(rows[0].keys()))
        for r in rows[:3]:
            print("  ", {k:(str(v)[:18] if v is not None else None) for k,v in list(r.items())[:8]})
        # null fraction per column
        import collections
        n=len(rows); nulls={k:sum(1 for r in rows if r.get(k) is None) for k in rows[0]}
        allnull=[k for k,c in nulls.items() if c==n]
        print("  all-null cols:", allnull, "| total rows:", n)
