from utils import install_ca, parse_census_excel
from subsets_utils import get
from constants import ENTITY_FILES
import collections
install_ca()
for eid in ["PC11_A02","PC11_A11"]:
    urls=ENTITY_FILES[eid]["urls"]
    print(f"\n== {eid}: {len(urls)} files ==")
    # parse first 3 files, look at state_code distribution + row counts
    allkeys=collections.Counter()
    total=0
    for u in urls[:4]:
        rows=parse_census_excel(get(u,timeout=(10,180)).content,u)
        sc=set(str(r.get('state_code')) for r in rows)
        total+=len(rows)
        print(f"  {u.rsplit('/',1)[-1][:30]:32s} rows={len(rows):5d} state_codes={sorted(sc)[:8]}")
