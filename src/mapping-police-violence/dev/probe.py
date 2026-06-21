import re
from collections import defaultdict
from subsets_utils import get
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SHARE = "https://airtable.com/appzVzSeINK1S3EVR/shroOenW19l1m3w0H/tblxearKzw8W7ViN8"
HEADERS = {
    "User-Agent": UA,
    "x-airtable-application-id": "appzVzSeINK1S3EVR",
    "x-airtable-inter-service-client": "webClient",
    "x-requested-with": "XMLHttpRequest",
    "x-time-zone": "America/New_York",
    "x-user-locale": "en",
    "Accept": "application/json",
}
html = get(SHARE, headers={"User-Agent": UA}, timeout=60).text
m = re.search(r'urlWithParams:\s*"([^"]+)"', html)
url = "https://airtable.com" + m.group(1).encode().decode("unicode_escape")
data = get(url, headers=HEADERS, timeout=180).json()
t = data["data"]["table"]
cols = t["columns"]; rows = t["rows"]
print("nrows", len(rows), "ncols", len(cols))
print("row keys:", list(rows[0].keys()))
types = defaultdict(set); samples = {}
for row in rows[:1000]:
    for cid, val in row["cellValuesByColumnId"].items():
        types[cid].add(type(val).__name__)
        if cid not in samples and val not in (None, "", []):
            samples[cid] = val
for c in cols:
    cid=c["id"]; s=samples.get(cid); sr=repr(s)
    if len(sr)>60: sr=sr[:60]+"..."
    print(f"{c['name']:34s} {c.get('type','?'):14s} {sorted(types.get(cid,[]))} {sr}")
