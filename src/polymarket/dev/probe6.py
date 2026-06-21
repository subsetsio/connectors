import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

base="https://gamma-api.polymarket.com/markets/keyset"
j0 = get(base, params={"limit":3}, timeout=(10,60)).json()
nc = j0["next_cursor"]
first_ids = [m["id"] for m in j0["markets"]]
print("page0 ids:", first_ids, "cursor:", nc[:20])

for pname in ["cursor","next_cursor","after","start_cursor","from"]:
    j = get(base, params={"limit":3, pname:nc}, timeout=(10,60)).json()
    if isinstance(j, dict) and "markets" in j:
        ids=[m["id"] for m in j["markets"]]
        print(f"param {pname:12}: ids={ids} {'ADVANCED' if ids!=first_ids else 'same'}")
    else:
        print(f"param {pname:12}: {str(j)[:120]}")
