import csv, io
from subsets_utils import get

def load(url):
    r = get(url, timeout=(10,120)); r.raise_for_status()
    return r.content.decode("utf-8", errors="replace")

for yr, url in [
  ("2010","https://www.countyhealthrankings.org/sites/default/files/analytic_data2010.csv"),
  ("2025","https://www.countyhealthrankings.org/sites/default/files/media/document/analytic_data2025_v3.csv"),
]:
    txt = load(url)
    rdr = csv.reader(io.StringIO(txt))
    header = next(rdr)
    # CHR sometimes has a second header row of long descriptions; check row2 first cell
    row1 = next(rdr)
    lc = [c.lower() for c in header]
    base = "premature death"
    cands = [c for c in lc if c.startswith(base) ]
    print(f"=== {yr}: ncols={len(header)}")
    print("  premature-death cols:", cands[:8])
    # show first-data-row sample for the premature death raw/num/denom/ci
    idx = {c:i for i,c in enumerate(lc)}
    for suf in [" raw value"," numerator"," denominator"," ci low"," ci high"]:
        k = base+suf
        print(f"   {k!r}:", (row1[idx[k]] if k in idx else "<MISSING COL>"))
    print("  row1 fips/name:", row1[:6])
