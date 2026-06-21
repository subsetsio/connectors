import re, json
from subsets_utils import get

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SHARE = "https://airtable.com/appzVzSeINK1S3EVR/shroOenW19l1m3w0H/tblxearKzw8W7ViN8"

html = get(SHARE, headers={"User-Agent": UA}, timeout=60).text
m = re.search(r'urlWithParams:\s*"([^"]+)"', html)
url = "https://airtable.com" + m.group(1).encode().decode("unicode_escape")
r = get(url, headers={
    "User-Agent": UA,
    "x-airtable-application-id": "appzVzSeINK1S3EVR",
    "x-airtable-inter-service-client": "webClient",
    "x-requested-with": "XMLHttpRequest",
    "Accept": "application/json",
}, timeout=180)
data = r.json()
t = data["data"]["table"]
cols = t["columns"]
id2 = {c["id"]: c for c in cols}
rows = t["rows"]
print("nrows", len(rows), "ncols", len(cols))
print("row top-level keys:", list(rows[0].keys()))
# inspect value type per column across a sample
from collections import defaultdict
types = defaultdict(set)
samples = {}
for row in rows[:500]:
    cv = row["cellValuesByColumnId"]
    for cid, val in cv.items():
        types[cid].add(type(val).__name__)
        if cid not in samples and val not in (None, "", []):
            samples[cid] = val
for c in cols:
    cid = c["id"]; nm = c["name"]
    s = samples.get(cid)
    sr = repr(s)
    if len(sr) > 70: sr = sr[:70]+"..."
    print(f"{nm:35s} airtype={c.get('type','?'):16s} pytypes={sorted(types.get(cid,[]))} sample={sr}")
