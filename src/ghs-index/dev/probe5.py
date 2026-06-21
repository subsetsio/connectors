import sys
sys.path.insert(0, "src")
from nodes import ghs_index as m
# 1) exercise the wayback path directly
txt = m._fetch_csv.__wrapped__ if hasattr(m._fetch_csv,"__wrapped__") else None
content = m._fetch_via_wayback(m.CSV_URL)
print("wayback bytes:", len(content))
# 2) full _fetch_csv (origin works locally -> origin path)
text = m._fetch_csv(m.CSV_URL)
import csv, io
rows = list(csv.reader(io.StringIO(text)))
print("rows incl header:", len(rows), "cols:", len(rows[0]))
print("header0:", repr(rows[0][0]))
