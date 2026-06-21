from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
checks=[
 # the 5 failures, at their failing page
 ("1a2b849de5d914ee33be7d126408f341",194,4),
 ("23e0cdd56bddb4ad3016a9c3ad63a539",29,7),
 ("35da7b3f137ea2fd15e7ae82db8ae966",6,1),
 ("e2bc3b33d169f2d0885cffb9183fb48e",28,1),
 ("ec7b2a0f066656833f1013b3a2f9f189",21,1),
]
import sys
big=eval(sys.argv[1]) if len(sys.argv)>1 else []
for ns,ds,dom in big:
    checks.append((ds,dom,1)); checks.append((ds,dom,2))
for ds,dom,pg in checks:
    try:
        r=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","page":pg,"page_size":50},timeout=(10,180))
        n=len(r.json().get("extension",{}).get("series",[])) if r.status_code==200 else 0
        print(f"{ds[:8]} dom{dom} pg{pg} ps50: {r.status_code} series={n}")
    except Exception as e:
        print(f"{ds[:8]} dom{dom} pg{pg} ps50: ERR {str(e)[:60]}")
