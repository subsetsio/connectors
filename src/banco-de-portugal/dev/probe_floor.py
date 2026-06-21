from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
# e2bc hardest; also test via series_ids batch approach
ds,dom="e2bc3b33d169f2d0885cffb9183fb48e",28
print("=== e2bc page1 at various ps ===")
for ps in [50,25,15,10,5]:
    r=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","page":1,"page_size":ps},timeout=(10,180))
    print(f"  ps={ps}: {r.status_code}")
# Now test series_ids approach: get a few series ids from a small page, then fetch by series_ids
r=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","page":1,"page_size":5},timeout=(10,180))
sids=[s["id"] for s in r.json()["extension"]["series"]]
print("sample sids:",sids)
print("=== fetch by series_ids batches ===")
for nb in [50,25,10]:
    # take first nb series ids — need more; just test with the 5 we have repeated logic: fetch 5 by id
    batch=",".join(str(x) for x in sids)
    rr=get(f"{BASE}/domains/{dom}/datasets/{ds}/",params={"lang":"EN","series_ids":batch},timeout=(10,180))
    print(f"  series_ids batch of {len(sids)}: {rr.status_code} series={len(rr.json().get('extension',{}).get('series',[])) if rr.status_code==200 else 0}")
    break
