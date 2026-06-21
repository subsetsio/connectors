from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
# ec7b: 70 series, page1 fails at ps=100
tests=[("ec7b2a0f066656833f1013b3a2f9f189",21,1),
       ("35da7b3f137ea2fd15e7ae82db8ae966",6,1)]
for ds,dom,pg in tests:
    print(f"\n=== {ds[:8]} dom{dom} page{pg} ===")
    for ps in [100,50,25,10,5]:
        try:
            r=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","page":pg,"page_size":ps},timeout=(10,180))
            n=len(r.json().get("extension",{}).get("series",[])) if r.status_code==200 else 0
            print(f"  ps={ps}: {r.status_code} series={n}")
        except Exception as e:
            print(f"  ps={ps}: ERR {str(e)[:60]}")
