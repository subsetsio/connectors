import json
import re
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def fetch(url):
    return get(url, headers=UA, timeout=(10, 180))


# marketshare sanitize and inspect structure
r = fetch("https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json")
txt = r.text
# count bare-* occurrences
print("bare-* count via regex ': *':", len(re.findall(r":\s*\*", txt)))
print("any '[ *' or ', *':", len(re.findall(r"[\[,]\s*\*\s*[,\]]", txt)))
san = re.sub(r":\s*\*", ": null", txt)
try:
    d = json.loads(san)
    print("parsed OK after sanitize")
    ms = d["pd"]["marketshare"]
    print("marketshare keys", list(ms.keys()))
    for k, v in ms.items():
        if isinstance(v, dict):
            print(" ", k, "-> dict keys", list(v.keys()))
            for kk, vv in v.items():
                if isinstance(vv, list):
                    print("      ", kk, "list len", len(vv), "item0", json.dumps(vv[0])[:200] if vv else "[]")
except Exception as e:
    print("still failing:", e)

# wide date ranges
print("=" * 60)
import datetime
today = datetime.date.today().isoformat()
for label, url in [
    ("rates secured wide", f"https://markets.newyorkfed.org/api/rates/secured/all/search.json?startDate=2000-01-01&endDate={today}"),
    ("tsy wide", f"https://markets.newyorkfed.org/api/tsy/all/results/summary/search.json?startDate=2000-01-01&endDate={today}"),
    ("rp wide", f"https://markets.newyorkfed.org/api/rp/results/search.json?startDate=2000-01-01&endDate={today}"),
    ("fxs wide", f"https://markets.newyorkfed.org/api/fxs/all/search.json?startDate=2000-01-01&endDate={today}"),
    ("seclending wide", f"https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate=2000-01-01&endDate={today}"),
    ("ambs wide", f"https://markets.newyorkfed.org/api/ambs/all/results/summary/search.json?startDate=2000-01-01&endDate={today}"),
]:
    r = fetch(url)
    try:
        d = r.json()
        top = list(d.keys())[0]
        inner = d[top]
        key = "auctions" if "auctions" in inner else ("operations" if "operations" in inner else list(inner.keys())[0])
        print(label, r.status_code, "->", top, key, "n=", len(inner[key]))
    except Exception as e:
        print(label, r.status_code, "ERR", e, r.text[:120])
