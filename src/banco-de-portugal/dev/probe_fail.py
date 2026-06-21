from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
fails=[(194,"1a2b849de5d914ee33be7d126408f341",4),
       (29,"23e0cdd56bddb4ad3016a9c3ad63a539",7),
       (6,"35da7b3f137ea2fd15e7ae82db8ae966",1),
       (28,"e2bc3b33d169f2d0885cffb9183fb48e",1),
       (21,"ec7b2a0f066656833f1013b3a2f9f189",1)]
for dom,ds,pg in fails:
    try:
        r=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","page":pg,"page_size":100},timeout=(10,180))
        n=len(r.json().get("extension",{}).get("series",[])) if r.status_code==200 else 0
        print(f"dom{dom} {ds[:8]} pg{pg}: {r.status_code} series={n} bytes={len(r.content)}")
    except Exception as e:
        print(f"dom{dom} {ds[:8]} pg{pg}: ERR {type(e).__name__} {str(e)[:80]}")
