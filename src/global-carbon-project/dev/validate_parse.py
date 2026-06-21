import sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import openpyxl
from nodes.global_carbon_project import _parse_global, _parse_national, SUBSETS, GLOBAL, NATIONAL, NATIONAL_MODEL

files = {
 "gcb": "/tmp/gcb/gcb2025.xlsx",
 "national_fossil": "/tmp/gcb/nat_fossil2025.xlsx",
 "national_luc": "/tmp/gcb/nat_luc2025.xlsx",
}
wbs = {k: openpyxl.load_workbook(v, read_only=True, data_only=True) for k,v in files.items()}
for eid,(fam,sheet,mode) in SUBSETS.items():
    wb = wbs[fam]
    if mode==GLOBAL:
        rows=_parse_global(wb[sheet])
    elif mode==NATIONAL:
        rows=_parse_national(wb[sheet])
    else:
        rows=[]
        for s in sheet: rows.extend(_parse_national(wb[s], model=s))
    n=len(rows)
    samp=rows[0] if rows else None
    if mode==GLOBAL:
        series=sorted(set(r["series"] for r in rows))
        extra=f"series={len(series)} yrs={min(r['year'] for r in rows)}-{max(r['year'] for r in rows)}"
    else:
        cs=sorted(set(r["country"] for r in rows))
        extra=f"countries={len(cs)} yrs={min(r['year'] for r in rows)}-{max(r['year'] for r in rows)}"
    print(f"{eid:42s} rows={n:7d}  {extra}")
    print(f"    sample={samp}")
