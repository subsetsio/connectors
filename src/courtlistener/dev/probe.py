import bz2, csv, io, sys
from subsets_utils import get

BASE = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/"

def header_and_rows(table, date="2026-03-31", n=3, maxbytes=400_000):
    url = f"{BASE}{table}-{date}.csv.bz2"
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    # only need the first chunk; decompress partial
    dec = bz2.BZ2Decompressor()
    raw = dec.decompress(r.content[:maxbytes]) if len(r.content) else b""
    text = raw.decode("utf-8", errors="replace")
    rdr = csv.reader(io.StringIO(text))
    rows = []
    for i, row in enumerate(rdr):
        rows.append(row)
        if i > n: break
    hdr = rows[0] if rows else []
    print(f"== {table} :: {len(hdr)} cols ==")
    print("COLS:", hdr)
    for row in rows[1:n+1]:
        print("ROW:", [ (c[:40]+'…') if len(c)>40 else c for c in row])
    print()

for t in ["courts","financial-disclosure-investments","people-db-people","people-db-positions","citation-map","fjc-integrated-database"]:
    try:
        header_and_rows(t)
    except Exception as e:
        print(f"!! {t}: {type(e).__name__}: {e}\n")
