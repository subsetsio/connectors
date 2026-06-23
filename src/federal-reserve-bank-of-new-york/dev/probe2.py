import json
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def fetch(url):
    return get(url, headers=UA, timeout=(10, 120))


# RP correct search path
r = fetch("https://markets.newyorkfed.org/api/rp/results/search.json?startDate=2024-01-01&endDate=2024-01-10")
print("RP results search", r.status_code)
d = r.json()
print("keys", list(d.keys()))
inner = d[list(d.keys())[0]]
print("inner keys", list(inner.keys()) if isinstance(inner, dict) else type(inner))
ops = inner["operations"] if isinstance(inner, dict) and "operations" in inner else inner
print("n ops", len(ops))
print(json.dumps(ops[0], indent=1)[:1200])

# PD bulk csv head
print("=" * 60)
r = fetch("https://markets.newyorkfed.org/api/pd/get/all/timeseries.csv")
print("PD bulk csv", r.status_code, "len", len(r.text))
lines = r.text.splitlines()
print("header:", lines[0][:300])
print("row1:", lines[1][:300])
print("nlines", len(lines))

# marketshare investigate
print("=" * 60)
r = fetch("https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json")
print("marketshare", r.status_code, "len", len(r.text))
print("around 19639:", repr(r.text[19600:19700]))
print("head:", r.text[:300])

# soma tsy monthly csv head
print("=" * 60)
r = fetch("https://markets.newyorkfed.org/api/soma/tsy/get/monthly.csv")
print("SOMA tsy monthly csv", r.status_code, "len", len(r.text))
lines = r.text.splitlines()
print("header:", lines[0][:300])
print("row1:", lines[1][:300])
print("nlines", len(lines))
