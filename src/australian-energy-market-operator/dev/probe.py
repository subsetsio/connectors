import csv, io
from subsets_utils import get

def fetch(region, ym):
    url = f"https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{ym}_{region}.csv"
    r = get(url, timeout=(10,120))
    return r

# valid recent
r = fetch("NSW1", "202605")
print("status", r.status_code, "len", len(r.content))
rows = list(csv.reader(io.StringIO(r.text)))
print("header", rows[0])
print("first", rows[1])
print("last", rows[-1])
print("nrows", len(rows)-1)

# earliest known
r2 = fetch("NSW1", "199812")
print("199812 NSW1 status", r2.status_code, "len", len(r2.content), "head", r2.text[:80].replace("\n","|"))

# future month -> expect 404/403
r3 = fetch("NSW1", "209901")
print("future status", r3.status_code, "len", len(r3.content), "head", r3.text[:120].replace("\n","|"))

# snowy historical
r4 = fetch("SNOWY1", "200001")
print("snowy 200001 status", r4.status_code, "len", len(r4.content), "head", r4.text[:80].replace("\n","|"))
