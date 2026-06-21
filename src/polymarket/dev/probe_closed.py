import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

def ks(**extra):
    p={"limit":5}; p.update(extra)
    r=get("https://gamma-api.polymarket.com/markets/keyset", params=p, timeout=(10,60))
    return r

# baseline
j=ks().json()
print("default: closed flags:", [m.get("closed") for m in j["markets"]])
# try closed=true
for params in [{"closed":"true"},{"closed":True},{"active":"false"},{"archived":"true"}]:
    r=ks(**params)
    if r.status_code==200:
        ms=r.json().get("markets",[])
        print(params, "->", [m.get("closed") for m in ms])
    else:
        print(params, "-> status", r.status_code, r.text[:100])
