import csv, io
from subsets_utils import get
r = get("https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/output-data/big-mac-full-index.csv", timeout=60)
r.raise_for_status()
rows = list(csv.DictReader(io.StringIO(r.text)))
print("rows:", len(rows))
cols = rows[0].keys()
print("cols:", list(cols))
# null/empty counts per column
from collections import Counter
empty = Counter()
for row in rows:
    for c in cols:
        if row[c] is None or row[c].strip() == "":
            empty[c]+=1
print("empty counts:", dict(empty))
dates = sorted(set(r["date"] for r in rows))
print("date min/max:", dates[0], dates[-1], "n_dates:", len(dates))
print("n countries:", len(set(r["iso_a3"] for r in rows)))
print("sample row:", rows[0])
