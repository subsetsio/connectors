from utils import install_ca, parse_census_excel
from subsets_utils import get
from constants import ENTITY_FILES
install_ca()
for eid, info in ENTITY_FILES.items():
    rows = parse_census_excel(get(info["urls"][0], timeout=(10,180)).content, info["urls"][0])
    print(f"\n== {eid} {info['table_code']} rows={len(rows)} cols={len(rows[0]) if rows else 0}")
    if rows:
        r=rows[1] if len(rows)>1 else rows[0]
        types={k:type(v).__name__ for k,v in r.items()}
        # show a numeric-looking col's type
        print("  sample row1 (first 9):", {k:v for k,v in list(r.items())[:9]})
        n=len(rows); allnull=[k for k in rows[0] if all(x.get(k) is None for x in rows)]
        numcols=[k for k in rows[0] if any(isinstance(x.get(k),(int,float)) for x in rows)]
        print(f"  numeric cols={len(numcols)} all-null cols={allnull}")
