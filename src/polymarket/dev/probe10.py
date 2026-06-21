import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

m = get("https://gamma-api.polymarket.com/markets/keyset", params={"limit":1}, timeout=(10,60)).json()["markets"][0]
print("TOP MARKET FIELDS:")
for k in ["id","question","slug","conditionId","outcomes","outcomePrices","volume","volumeNum","liquidity","liquidityNum","active","closed","createdAt","updatedAt","startDate","endDate","category","clobTokenIds"]:
    print(f"  {k}: ({type(m.get(k)).__name__}) {str(m.get(k))[:60]}")
ev = m["events"][0]
print("\nEMBEDDED EVENT KEYS:", sorted(ev.keys()))

# event endpoint fields
e = get("https://gamma-api.polymarket.com/events/keyset", params={"limit":1}, timeout=(10,60)).json()["events"][0]
print("\nEVENT FIELDS:")
for k,v in e.items():
    if k in ("markets","series","tags"): 
        print(f"  {k}: ({type(v).__name__}) len={len(v) if isinstance(v,list) else '-'}")
    else:
        print(f"  {k}: ({type(v).__name__}) {str(v)[:50]}")

# filter params for volume?
print("\n== try volume_num_min filter ==")
r = get("https://gamma-api.polymarket.com/markets", params={"limit":3,"volume_num_min":100000,"order":"volumeNum","ascending":"false"}, timeout=(10,60))
j=r.json()
print("status",r.status_code,"type",type(j).__name__)
if isinstance(j,list):
    print("vols:", [round(x.get("volumeNum") or 0) for x in j])
