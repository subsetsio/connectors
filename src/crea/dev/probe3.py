import io, zipfile
from collections import Counter
import openpyxl
import sys
sys.path.insert(0, "src")
from nodes.crea import _zip_url, _fetch_bytes, _rows_from_sheet, _WORKBOOKS

data = _fetch_bytes(_zip_url())
zf = zipfile.ZipFile(io.BytesIO(data))
recs = []
for fname, freq, sa in _WORKBOOKS:
    wb = openpyxl.load_workbook(io.BytesIO(zf.read(fname)), read_only=True)
    for sheet in wb.sheetnames:
        recs.extend(_rows_from_sheet(wb[sheet], sheet, freq, sa))
    wb.close()

print("total records:", len(recs))
print("freq:", Counter(r["frequency"] for r in recs))
print("levels:", Counter(r["level"] for r in recs))
print("housing_types:", Counter(r["housing_type"] for r in recs))
print("geographies:", len(set(r["geography"] for r in recs)))
print("sa values:", Counter(r["seasonally_adjusted"] for r in recs))
dmin = min(r["date"] for r in recs); dmax = max(r["date"] for r in recs)
print("date range:", dmin, "->", dmax)
hpi = [r["hpi_index"] for r in recs if r["hpi_index"] is not None]
bm = [r["benchmark_price"] for r in recs if r["benchmark_price"] is not None]
print("hpi_index: n=%d min=%.1f max=%.1f" % (len(hpi), min(hpi), max(hpi)))
print("benchmark: n=%d min=%.0f max=%.0f" % (len(bm), min(bm), max(bm)))
print("null hpi:", sum(1 for r in recs if r["hpi_index"] is None))
print("null bm:", sum(1 for r in recs if r["benchmark_price"] is None))
import datetime
print("sample:", recs[0])
# uniqueness of key
keys = Counter((r["date"], r["geography"], r["housing_type"], r["frequency"], r["seasonally_adjusted"]) for r in recs)
dups = [k for k,c in keys.items() if c>1]
print("dup keys:", len(dups))
