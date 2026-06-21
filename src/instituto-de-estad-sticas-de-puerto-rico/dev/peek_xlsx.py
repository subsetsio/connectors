import io
import pandas as pd
import nodes.instituto_de_estad_sticas_de_puerto_rico as m
m._ensure_http()
def peek(pkg):
    res=m._api("package_show",id=pkg)["resources"]
    for r in res:
        fmt=(r.get('format') or '').upper()
        print(f"\n##### {pkg} :: {r.get('name')} [{fmt}]")
        if fmt in ('XLSX','XLS'):
            c=m._download_bytes(r['url'])
            xl=pd.ExcelFile(io.BytesIO(c), engine='openpyxl' if fmt=='XLSX' else 'xlrd')
            print("  sheets:", xl.sheet_names[:6])
            g=xl.parse(xl.sheet_names[0], header=None, dtype=str).where(lambda d:d.notna(), None).values.tolist()
            for i,row in enumerate(g[:12]):
                nn=[ (j,str(v)[:18]) for j,v in enumerate(row) if v is not None and str(v).strip()!='']
                print(f"   r{i} ({len(nn)}nn): {nn[:6]}")
        elif fmt=='CSV':
            c=m._download_bytes(r['url'])
            txt=m._decode(c[:500])
            print("   csv head:", repr(txt[:200]))
        break  # only first resource for brevity
for p in ["ghgrp","directorio-de-instituciones-de-educacion-superior-puerto-rico"]:
    peek(p)
