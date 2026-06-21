import sys
sys.path.insert(0,"src")
from nodes.nhs_digital import _ckan_package, _download_bytes, _iter_tables, _clean, _DATA_EXT

def select(pkg):
    rec=_ckan_package(pkg)
    urls=[]
    for r in rec["resources"]:
        u=r.get("url") or ""; m=_DATA_EXT.search(u.split("?")[0])
        if "files.digital.nhs.uk" in u and m: urls.append((u,m.group(1).lower()))
    if any(e=="csv" for _,e in urls):
        urls=[(u,e) for u,e in urls if e in ("csv","zip")]
    return urls

for pkg in ["general_pharmaceutical_services","national-diabetes-inpatient-audit-nadia-2019"]:
    urls=select(pkg)
    print(f"\n== {pkg}: selected {len(urls)} files: {[e for _,e in urls]}")
    cells=0
    for u,ext in urls:
        c=_download_bytes(u)
        for src,rows in _iter_tables(ext,c,u.split('?')[0].rsplit('/',1)[-1]):
            if not rows: continue
            n=sum(1 for row in rows[1:] for cell in row if _clean(cell) is not None)
            cells+=n
            print(f"   {src[:55]:55} rows={len(rows)} cells={n}")
    print("   TOTAL cells:", cells)
