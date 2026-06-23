import csv, io, datetime
from subsets_utils import get

BASE = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/"
FILES = {
    "big-mac-full-index": "output-data/big-mac-full-index.csv",
    "big-mac-raw-index": "output-data/big-mac-raw-index.csv",
    "big-mac-adjusted-index": "output-data/big-mac-adjusted-index.csv",
    "big-mac-source-data": "source-data/big-mac-source-data-v2.csv",
    "big-mac-historical-source-data": "source-data/big-mac-historical-source-data.csv",
}

for eid, path in FILES.items():
    r = get(BASE + path, timeout=(10, 120))
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    hdr = list(rows[0].keys())
    dates = sorted({row["date"][:10] for row in rows})
    print(f"== {eid}: {len(rows)} rows")
    print("   header:", hdr)
    print("   date span:", dates[0], "->", dates[-1], f"({len(dates)} distinct)")
    # confirm date parse
    datetime.date.fromisoformat(rows[0]["date"][:10])
    # check uniqueness of (date, iso_a3)
    keys = [(row["date"][:10], row.get("iso_a3")) for row in rows]
    print("   (date,iso_a3) unique:", len(keys) == len(set(keys)))
    # show a couple sample numeric values / blanks
    blanks = sum(1 for row in rows for v in row.values() if v == "")
    print("   blank cells:", blanks)
