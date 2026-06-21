import csv, io
from subsets_utils import get

def fetch(year):
    r = get(f"https://rsf.org/sites/default/files/import_classement/{year}.csv", timeout=(10, 120))
    r.raise_for_status()
    return r.content

for year in (2002, 2013, 2021, 2022, 2026):
    raw = fetch(year)
    text = raw.decode("utf-8-sig", errors="replace")
    if not text.strip():
        print(f"=== {year}: EMPTY ===")
        continue
    rdr = csv.DictReader(io.StringIO(text), delimiter=";")
    rows = list(rdr)
    print(f"=== {year}: {len(rows)} rows ===")
    print("  cols:", rdr.fieldnames)
    print("  row0:", {k: rows[0][k] for k in rdr.fieldnames})
