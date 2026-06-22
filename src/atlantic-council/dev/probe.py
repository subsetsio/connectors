import sys; sys.path.insert(0, "src")
from subsets_utils import get
BASE="https://freedom-and-prosperity-indexes.atlanticcouncil.org/data/processed"
def g(p): 
    r=get(f"{BASE}/{p}", timeout=(10,60)); r.raise_for_status(); return r.json()
cp=g("chartProfiles/afg.json")
print("chartProfiles len:",len(cp),"years",cp[0]["indexYear"],"->",cp[-1]["indexYear"])
r=cp[0]
print("KEYS:",list(r.keys()))
import json
print("rec0:",json.dumps(r,indent=0)[:1500])
cm=g("countriesManifest.json")
print("countries:",len(cm),"sample keys",list(cm[0].keys()))
gm=g("groupingsManifest.json")
print("grouping keys:",{k:len(v) for k,v in gm.items()})
# probe a grouping chartProfile
gp=g("chartProfiles/global.json")
print("global cp len",len(gp),"rec0 freedomIndex",gp[0].get("freedomIndex"),"rank",gp[0].get("freedomIndexRank"))
