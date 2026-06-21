import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
def count(closed, vmin=100000):
    off=0;n=0
    while True:
        r=get("https://gamma-api.polymarket.com/markets",
              params={"limit":100,"offset":off,"volume_num_min":vmin,"closed":closed,
                      "order":"volumeNum","ascending":"false"},timeout=(10,60))
        if r.status_code!=200: return f">{n} (cap at {off})"
        j=r.json()
        if not isinstance(j,list) or not j: break
        n+=len(j)
        if len(j)<100: break
        off+=100
        if off>3000: return f">{n} (offset cap)"
    return n
for c in ("false","true"):
    print(f"closed={c} volume>=100k: {count(c)} markets")
