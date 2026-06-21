import sys
sys.path.insert(0, "src")
from nodes.cru import _parse_per, _fetch_text, CY_BASE, _list_per_files

files = _list_per_files("pre")
print("pre files:", len(files))
txt = _fetch_text(f"{CY_BASE}/pre/{files[10]}")
rows = _parse_per(txt, "pre")
print("rows from one pre file:", len(rows))
print("sample:", rows[0])
print("periods seen:", sorted({r["period"] for r in rows}))
print("years:", min(r["year"] for r in rows), "-", max(r["year"] for r in rows))
print("units:", rows[0]["units"], "| parameter:", rows[0]["parameter"])
