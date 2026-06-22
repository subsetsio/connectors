import json, time
from subsets_utils import get

BASE = "https://transfermarkt-api.fly.dev"

def show(label, url):
    t0 = time.time()
    r = get(url, timeout=(10.0, 120.0))
    dt = time.time() - t0
    print(f"\n=== {label}  [{r.status_code}] {dt:.1f}s  {url}")
    try:
        j = r.json()
    except Exception as e:
        print("non-json:", r.text[:300]); return None
    print(json.dumps(j, indent=2)[:1800])
    return j

# rate-limit burst test: 6 quick calls
print("### burst test")
for i in range(6):
    t0 = time.time()
    r = get(f"{BASE}/competitions/search/premier?page_number=1", timeout=(10.0, 60.0))
    print(f"  call {i}: {r.status_code} in {time.time()-t0:.2f}s  retry-after={r.headers.get('retry-after')}")

comp = show("competitions/GB1/clubs", f"{BASE}/competitions/GB1/clubs")
clubs_list = comp.get("clubs") if comp else None
club_id = clubs_list[0]["id"] if clubs_list else "281"
show("clubs/{id}/profile", f"{BASE}/clubs/{club_id}/profile")
pl = show("clubs/{id}/players", f"{BASE}/clubs/{club_id}/players")
players = pl.get("players") if pl else None
pid = players[0]["id"] if players else "28003"
show("players/{id}/profile", f"{BASE}/players/{pid}/profile")
show("players/{id}/market_value", f"{BASE}/players/{pid}/market_value")
show("players/{id}/transfers", f"{BASE}/players/{pid}/transfers")
show("players/{id}/stats", f"{BASE}/players/{pid}/stats")
show("players/{id}/injuries", f"{BASE}/players/{pid}/injuries")
