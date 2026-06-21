import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def count_above(vmin):
    # walk offset endpoint (sorted desc by volume) within filtered set
    off=0; n=0
    while True:
        r=get("https://gamma-api.polymarket.com/markets",
              params={"limit":100,"offset":off,"volume_num_min":vmin,"order":"volumeNum","ascending":"false"},
              timeout=(10,60))
        if r.status_code!=200: 
            return f">{n} (offset cap hit at {off}: {r.text[:60]})"
        j=r.json()
        if not isinstance(j,list) or not j: break
        n+=len(j); 
        if len(j)<100: break
        off+=100
        if off>=5000: return f">={n} (offset cap)"
    return n

for v in [100000, 50000, 25000, 10000]:
    print(f"volume>={v}: {count_above(v)} markets")
