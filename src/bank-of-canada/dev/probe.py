import json
from subsets_utils import get

def show(url, **kw):
    print("=" * 80)
    print("GET", url, kw or "")
    r = get(url, timeout=(10.0, 120.0), **kw)
    print("status", r.status_code, "ctype", r.headers.get("content-type"))
    try:
        j = r.json()
    except Exception as e:
        print("non-json", e, r.text[:300])
        return None
    return j

# 1. groups list
g = show("https://www.bankofcanada.ca/valet/lists/groups/json")
if g:
    groups = g.get("groups", {})
    print("num groups:", len(groups))
    sample = list(groups.items())[:3]
    print(json.dumps(sample, indent=2)[:1500])

# 2. series list
s = show("https://www.bankofcanada.ca/valet/lists/series/json")
if s:
    series = s.get("series", {})
    print("num series:", len(series))
    sample = list(series.items())[:3]
    print(json.dumps(sample, indent=2)[:1500])

# 3. observations for a single series
o = show("https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json", params={"recent": 3})
if o:
    print("top keys:", list(o.keys()))
    print("seriesDetail:", json.dumps(o.get("seriesDetail"), indent=2)[:800])
    print("observations sample:", json.dumps(o.get("observations", [])[:3], indent=2)[:800])

# 4. per-group observations
og = show("https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json", params={"recent": 2})
if og:
    print("top keys:", list(og.keys()))
    print("groupDetail:", json.dumps(og.get("groupDetail"), indent=2)[:600])
    sd = og.get("seriesDetail", {})
    print("num series in group:", len(sd))
    print("observations sample:", json.dumps(og.get("observations", [])[:2], indent=2)[:1000])
