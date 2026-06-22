import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
import nodes.bcrd as M
from constants import FILES_BY_SPEC

for sid in ["bcrd-precios-ipc", "bcrd-sector-real-pib",
            "bcrd-mercado-de-trabajo-tasa-desocupacion-fa",
            "bcrd-sector-monetario-y-financiero-tasas-diariasbac"]:
    if sid not in FILES_BY_SPEC:
        print("MISSING", sid); continue
    paths = FILES_BY_SPEC[sid]
    print("="*60, sid, f"({len(paths)} files)")
    rows=[]
    for p in paths[:2]:
        fn=p.rsplit("/",1)[-1]
        try:
            content=M._download(M.CDN_BASE+p)
        except Exception as e:
            print("  dl err", fn, type(e).__name__, getattr(getattr(e,'response',None),'status_code',None)); continue
        sheets=M._read_sheets(content, fn)
        cs=M._cells(sheets, fn)
        rows.extend(cs)
        print(f"  {fn}: {len(cs)} cells, sheets={list(sheets)[:4]}")
    nums=[r for r in rows if r['num'] is not None]
    print(f"  TOTAL cells={len(rows)} numeric={len(nums)}")
    for r in rows[:4]+nums[:3]:
        print("   ", r)
