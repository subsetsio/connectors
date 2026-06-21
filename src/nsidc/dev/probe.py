import csv, io
from subsets_utils import get

BASE = "https://noaadata.apps.nsidc.org/NOAA/G02135"

def show(url, n=6):
    r = get(url, timeout=(10, 120))
    r.raise_for_status()
    print("==== ", url, " status", r.status_code, "len", len(r.text))
    lines = r.text.splitlines()
    for ln in lines[:n]:
        print(repr(ln))
    print("... tail:")
    for ln in lines[-3:]:
        print(repr(ln))
    return r.text

# daily north
d = show(f"{BASE}/north/daily/data/N_seaice_extent_daily_v4.0.csv")
# monthly north 09
m = show(f"{BASE}/north/monthly/data/N_09_extent_v4.0.csv")
# climatology north
c = show(f"{BASE}/north/daily/data/N_seaice_extent_climatology_1981-2010_v4.0.csv")

# check monthly for sentinel / blanks across a low-coverage month (e.g. Jan early antarctic)
ms = show(f"{BASE}/south/monthly/data/S_01_extent_v4.0.csv", n=8)

# parse daily to check sentinel handling and value ranges
reader = list(csv.reader(io.StringIO(d)))
print("daily header:", reader[0])
print("daily units :", reader[1])
print("daily row3  :", reader[2])
# count -9999 in extent
extent_idx = [h.strip() for h in reader[0]].index("Extent")
miss_idx = [h.strip() for h in reader[0]].index("Missing")
vals = [r[extent_idx].strip() for r in reader[2:] if len(r) > extent_idx]
print("daily n rows:", len(vals), "min/max extent (raw str sample):", vals[:3], vals[-3:])
print("any -9999 extent:", any(v == "-9999" for v in vals))
