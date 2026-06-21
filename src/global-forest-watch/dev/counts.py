import subsets_utils as su, json
BASE="https://data-api.globalforestwatch.org"
ents=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/global-forest-watch/work/entity_union.json"))
ids=ents if isinstance(ents,list) else ents.get("entities") or list(ents.keys())
print("n entities", len(ids))
def resolve(name):
    r=su.get(f"{BASE}/dataset/{name}", timeout=60)
    vs=r.json()["data"]["versions"]
    return max(vs)  # lexicographic max
for name in sorted(ids):
    try:
        v=resolve(name)
        r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv", params={"sql":"SELECT count(*) AS n FROM data"}, timeout=180)
        if r.status_code==200:
            n=int(r.text.strip().splitlines()[-1])
            print(f"{n:>12}  {name}  {v}")
        else:
            print(f"{'ERR':>12}  {name}  {v}  {r.status_code} {r.text[:80]}")
    except Exception as e:
        print(f"{'EXC':>12}  {name}  {type(e).__name__} {e}")
