import csv, io
from subsets_utils import get, configure_http

configure_http(headers={"User-Agent": "subsets.io RBA statistics connector (+https://subsets.io)"})

SAMPLES = ["g1-data", "a2-data", "a3-daily-open-market-operations",
           "b12.1.1-africa-and-middle-east", "j1-cash-rate", "h5-data", "f11.1-data"]

for slug in SAMPLES:
    url = f"https://www.rba.gov.au/statistics/tables/csv/{slug}.csv"
    r = get(url, timeout=(10,60))
    text = r.content.decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    print("="*90)
    print(f"{slug}: status={r.status_code} nrows={len(rows)} ncols={max((len(x) for x in rows), default=0)}")
    for i, row in enumerate(rows[:13]):
        print(f"  r{i} [{len(row)}]: {row[:5]}")
    print("  last:", rows[-1][:5] if rows else None)
