import json,re
from subsets_utils import get
for period in ("qtrly","ytd"):
    r=get(f"https://markets.newyorkfed.org/api/marketshare/{period}/latest.json",timeout=(10,60))
    d=json.loads(re.sub(r":\s*\*",": null",r.text))
    ms=d["pd"]["marketshare"]
    print(period,"ms keys:",list(ms.keys()))
    grp=ms[list(ms.keys())[0]]
    print("  grp keys:",list(grp.keys()))
    print("  item keys:",list(grp["totals"][0].keys()))
    print("  item sample:",json.dumps(grp["totals"][0])[:400])
