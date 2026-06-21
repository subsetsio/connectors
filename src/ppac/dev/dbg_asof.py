import sys, importlib
sys.path.insert(0,"src")
mod=importlib.import_module("nodes.ppac")
url=mod._discover_xlsx_url("consumption/active-domestic-customers")
print("url:",url)
wb=mod._load_xlsx(url); ws=wb.worksheets[0]
rs=mod._rows_of(ws)
hdr=mod._find_row(rs, lambda r: bool(r) and str(r[0] or "").strip().upper().startswith("STATE"))
print("hdr idx:",hdr,"row:",rs[hdr][:3] if hdr is not None else None)
print("as_of:",mod._as_date_str(rs[hdr][1]) if hdr is not None else None)
