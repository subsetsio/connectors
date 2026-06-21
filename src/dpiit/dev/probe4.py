import sys; sys.path.insert(0, "src")
from nodes import dpiit as m

# WPI parse
header, rows = m._load_wpi_monthly()
n_items = sum(1 for r in m._wpi_records(header, rows) if r[3] is None)
vals = [r for r in m._wpi_records(header, rows) if r[3] is not None]
print("WPI items:", n_items, "value records:", len(vals))
print("sample value:", vals[0])
print("date range:", min(r[3] for r in vals), "->", max(r[3] for r in vals))

# Core parse
import io, openpyxl
url = m._discover(r"eight_core_infra/Core_Industries_2011_12_\d{8}\.xlsx")
wb = openpyxl.load_workbook(io.BytesIO(m._fetch_bytes(url)), read_only=True, data_only=True)
idx = m._parse_core_sheet(wb, "Index")
grw = m._parse_core_sheet(wb, "Growth (%)")
print("core index cells:", len(idx), "growth cells:", len(grw))
print("sectors:", sorted(set(s for _,s in idx)))
print("core date range:", min(d for d,_ in idx), "->", max(d for d,_ in idx))
print("sample with growth:", [( (d,s), idx[(d,s)], grw.get((d,s)) ) for (d,s) in list(idx)[:2]])
