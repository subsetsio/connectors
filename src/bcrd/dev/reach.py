import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from constants import FILES_BY_SPEC
from subsets_utils import get
import concurrent.futures as cf

def check(item):
    sid, paths = item
    p = paths[0]
    try:
        r = get("https://cdn.bancentral.gov.do/"+p, timeout=(8,40))
        return sid, r.status_code, len(paths)
    except Exception as e:
        return sid, "ERR:"+type(e).__name__, len(paths)

items=list(FILES_BY_SPEC.items())
results=[]
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for r in ex.map(check, items):
        results.append(r)

tally=collections.Counter(r[1] for r in results)
print("status tally (first-file of each of %d specs):"%len(items), dict(tally))
bad=[(sid,st,n) for sid,st,n in results if st!=200]
print("non-200 specs:",len(bad))
for sid,st,n in sorted(bad)[:60]:
    print(f"  {st}  {sid}  ({n} files)")
