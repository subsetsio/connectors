import bz2, csv, io
from subsets_utils import get

BASE = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/"

def header_and_rows(table, date="2026-03-31", n=2, maxbytes=300_000):
    url = f"{BASE}{table}-{date}.csv.bz2"
    r = get(url, timeout=(10,120), headers={"Range": f"bytes=0-{maxbytes}"})
    dec = bz2.BZ2Decompressor()
    try:
        raw = dec.decompress(r.content)
    except Exception as e:
        raw = getattr(dec, "unused_data", b"") or b""
    text = raw.decode("utf-8", errors="replace")
    rdr = csv.reader(io.StringIO(text))
    rows = []
    for i, row in enumerate(rdr):
        rows.append(row)
        if i > n: break
    hdr = rows[0] if rows else []
    print(f"== {table} :: {len(hdr)} cols :: status={r.status_code} ==")
    print("COLS:", hdr)
    for row in rows[1:n+1]:
        print("ROW:", [ (c[:35]+'…') if len(c)>35 else c for c in row])
    print()

for t in ["courts","financial-disclosure-investments","financial-disclosures","people-db-people","people-db-positions","people-db-political-affiliations","citations","fjc-integrated-database","oral-arguments","parentheticals"]:
    try:
        header_and_rows(t)
    except Exception as e:
        print(f"!! {t}: {type(e).__name__}: {e}\n")
