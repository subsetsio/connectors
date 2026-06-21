import csv
import io
from subsets_utils import get

CATALOG = "https://cdn.cboe.com/api/global/us_indices/definitions/GlobalIndices.csv"

r = get(CATALOG, timeout=(10.0, 120.0))
print("catalog status", r.status_code, "len", len(r.text))
rows = list(csv.reader(io.StringIO(r.text)))
print("header:", rows[0])
print("n rows:", len(rows) - 1)
for row in rows[1:6]:
    print(row)

# Look at a few symbol shapes
def show_hist(sym):
    fname = sym.lstrip(".")
    url = f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{fname}_History.csv"
    rr = get(url, timeout=(10.0, 120.0))
    print("\n===", sym, "->", url, "status", rr.status_code)
    if rr.status_code != 200:
        print("  body head:", rr.text[:200])
        return
    hr = list(csv.reader(io.StringIO(rr.text)))
    print("  header:", hr[0], "nrows", len(hr) - 1)
    for x in hr[1:4]:
        print("  ", x)
    for x in hr[-2:]:
        print("  ...", x)

for s in ["VIX", "SPX", "OEX", "SKEW"]:
    show_hist(s)

# Check a dotted symbol
dotted = [r[0] for r in rows[1:] if r and r[0].startswith(".")][:3]
print("\ndotted samples:", dotted)
for s in dotted[:2]:
    show_hist(s)
