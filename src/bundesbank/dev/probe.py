from subsets_utils import get

# Probe a small dataflow CSV
url = "https://api.statistiken.bundesbank.de/rest/data/BBZVS01?format=csv"
r = get(url, timeout=(10,120))
print("status", r.status_code)
print("content-type", r.headers.get("content-type"))
print("len", len(r.content))
text = r.text
lines = text.splitlines()
print("nlines", len(lines))
for ln in lines[:6]:
    print(repr(ln[:400]))
