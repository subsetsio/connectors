import json
from subsets_utils import get
from extract import extract_workbook

paths = json.load(open("dev/paths.json"))
union = json.load(open("../../../data/sources/florida-office-of-economic-and-demographic-research/work/entity_union.json"))
ROOT = "https://edr.state.fl.us"

low = []
errs = []
for n, eid in enumerate(union):
    try:
        r = get(ROOT + paths[eid], timeout=(10, 120))
        r.raise_for_status()
        recs = extract_workbook(r.content)
        c = len(recs)
        if c < 5:
            low.append((eid, c))
        print(f"{n+1:3d}/{len(union)} {c:7d}  {eid}")
    except Exception as ex:
        errs.append((eid, f"{type(ex).__name__}: {ex}"))
        print(f"{n+1:3d}/{len(union)} ERROR   {eid}: {type(ex).__name__}: {ex}")

print("\n==== LOW (<5 records) ====")
for e, c in low:
    print(" ", c, e)
print("==== ERRORS ====")
for e, m in errs:
    print(" ", e, m)
print(f"\ntotal={len(union)} low={len(low)} errors={len(errs)}")
