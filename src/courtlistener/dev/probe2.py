import bz2, csv, io
from subsets_utils import get
BASE = "https://com-courtlistener-storage.s3-us-west-2.amazonaws.com/bulk-data/"
def hdr(table, date="2026-03-31", maxbytes=200_000):
    url = f"{BASE}{table}-{date}.csv.bz2"
    r = get(url, timeout=(10,120), headers={"Range": f"bytes=0-{maxbytes}"})
    dec = bz2.BZ2Decompressor()
    raw = dec.decompress(r.content)
    text = raw.decode("utf-8", errors="replace")
    row = next(csv.reader(io.StringIO(text)))
    print(f'    "{table}": {row},')
for t in ["citation-map","dockets","opinion-clusters","financial-disclosures-agreements","financial-disclosures-debts","financial-disclosures-gifts","financial-disclosures-non-investment-income","financial-disclosures-positions","financial-disclosures-reimbursements","financial-disclosures-spousal-income"]:
    try: hdr(t)
    except Exception as e: print(f"!! {t}: {type(e).__name__}: {e}")
