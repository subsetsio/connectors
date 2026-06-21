import io, csv
from collections import Counter
from subsets_utils import get

URL = "https://data.un.org/_Docs/SYB/CSV/SYB67_176_202411_Tourist-Visitors%20Arrival%20and%20Expenditure.csv"
r = get(URL, timeout=(10.0,120.0)); r.raise_for_status()
lines = r.text.split("\n")
reader = csv.DictReader(io.StringIO("\n".join(lines[1:])))
key_series = Counter()
years = Counter()
non_numeric_codes = set()
sample_high_codes = {}
for row in reader:
    code = row["Region/Country/Area"].strip()
    name = row[""].strip()
    year = row["Year"].strip()
    series = row["Series"].strip()
    years[year]+=1
    key_series[(code,year,series)] += 1
    if not code.isdigit():
        non_numeric_codes.add(code)
    ci = int(code) if code.isdigit() else -1
    if ci >= 900:
        sample_high_codes[ci] = name
dups = {k:v for k,v in key_series.items() if v>1}
print("duplicate (code,year,series) count:", len(dups))
for k,v in list(dups.items())[:10]: print("  DUP", k, v)
print("years:", dict(sorted(years.items())))
print("non-numeric codes:", non_numeric_codes)
print("high M49 codes (>=900, aggregates):", dict(sorted(sample_high_codes.items())))
