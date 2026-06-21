import csv, io
from subsets_utils import get, configure_http
configure_http(headers={"User-Agent": "subsets.io RBA statistics connector (+https://subsets.io)"})
for slug in ["a5-data","c9-data","d10-data"]:
    r=get(f"https://www.rba.gov.au/statistics/tables/csv/{slug}.csv", timeout=(10,60))
    rows=list(csv.reader(io.StringIO(r.content.decode("utf-8-sig",errors="replace"))))
    print("="*80); print(f"{slug}: status={r.status_code} nrows={len(rows)}")
    for i,row in enumerate(rows[:16]):
        print(f"  r{i}[{len(row)}]: {row[:5]}")
