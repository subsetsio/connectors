import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

# full field dump of one market and one event
m = get("https://gamma-api.polymarket.com/markets/keyset", params={"limit":1}, timeout=(10,60)).json()["markets"][0]
print("MARKET FIELDS:")
for k,v in m.items():
    vs = str(v)[:70]
    print(f"  {k}: ({type(v).__name__}) {vs}")
