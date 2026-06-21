import io, csv
from subsets_utils import get

URL = "https://data.un.org/_Docs/SYB/CSV/SYB67_176_202411_Tourist-Visitors%20Arrival%20and%20Expenditure.csv"
r = get(URL, timeout=(10.0, 120.0))
r.raise_for_status()
text = r.text
lines = text.split("\n")
print("=== status:", r.status_code, "bytes:", len(text), "total lines:", len(lines))
print("=== line0 (banner):", repr(lines[0]))
print("=== line1 (header):", repr(lines[1]))
print("=== line2:", repr(lines[2]))
print("=== line3:", repr(lines[3]))

# Parse skipping banner
reader = csv.DictReader(io.StringIO("\n".join(lines[1:])))
print("=== fieldnames:", reader.fieldnames)
series_set = set()
type_set = set()
years = set()
n = 0
sample = []
for row in reader:
    n += 1
    series_set.add(row.get("Series","").strip())
    t = row.get("Tourism arrivals series type","").strip()
    if t: type_set.add(t)
    y = row.get("Year","").strip()
    if y: years.add(y)
    if n <= 4: sample.append(row)
print("=== total data rows:", n)
print("=== distinct Series:", series_set)
print("=== distinct arrivals types:", type_set)
print("=== year range:", min(years), max(years), "distinct years:", len(years))
print("=== sample rows:")
for s in sample:
    print(s)
