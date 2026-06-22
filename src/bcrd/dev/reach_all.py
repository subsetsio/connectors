import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from constants import FILES_BY_SPEC
from subsets_utils import get
import concurrent.futures as cf

pairs=[(sid,p) for sid,ps in FILES_BY_SPEC.items() for p in ps]
def check(item):
    sid,p=item
    try:
        r=get("https://cdn.bancentral.gov.do/"+p, timeout=(8,40))
        return sid,p,r.status_code
    except Exception as e:
        return sid,p,"ERR:"+type(e).__name__

res=[]
with cf.ThreadPoolExecutor(max_workers=24) as ex:
    for r in ex.map(check,pairs): res.append(r)
tally=collections.Counter(r[2] for r in res)
print(f"checked {len(pairs)} files:",dict(tally))
bad=[(sid,p,st) for sid,p,st in res if st!=200]
# group bad by spec
byspec=collections.defaultdict(list)
for sid,p,st in bad: byspec[sid].append((p,st))
print("specs with >=1 bad file:",len(byspec))
# specs where ALL files bad (these would fail the node)
allbad=[sid for sid in byspec if len(byspec[sid])==len(FILES_BY_SPEC[sid])]
print("specs where ALL files bad (NODE WOULD FAIL):",len(allbad))
for sid in allbad: print("   FAIL",sid, FILES_BY_SPEC[sid])
print("--- sample partial-bad ---")
for sid in list(byspec)[:10]:
    if sid not in allbad:
        print(f"  {sid}: {len(byspec[sid])}/{len(FILES_BY_SPEC[sid])} bad e.g. {byspec[sid][0]}")
