import sys
sys.path.insert(0, "src")
from nodes.nhs_digital import _ckan_package, _download_bytes, _iter_tables, _clean, _DATA_EXT

def melt_count(pkg, limit_files=3):
    rec=_ckan_package(pkg)
    urls=[r["url"] for r in rec["resources"] if "files.digital.nhs.uk" in (r.get("url") or "") and _DATA_EXT.search(r["url"].split("?")[0])]
    print(f"\n== {pkg}: {len(urls)} live files (sampling {min(limit_files,len(urls))})")
    cells=0
    for u in urls[:limit_files]:
        base=u.split("?")[0]; ext=base.rsplit(".",1)[-1].lower()
        content=_download_bytes(u)
        for src,rows in _iter_tables(ext, content, base.rsplit("/",1)[-1]):
            if not rows: 
                print("   (empty)", src); continue
            header=[_clean(c) for c in rows[0]]
            nice=[h for h in header if h][:8]
            c=sum(1 for row in rows[1:] for cell in row if _clean(cell) is not None)
            cells+=c
            print(f"   {src[:60]:60} rows={len(rows)} cols={len(header)} hdr={nice} cells={c}")
    print("   sampled cells:", cells)

for p in ["national-diabetes-inpatient-safety-audit-ndisa-2018-2021",
          "general_pharmaceutical_services",
          "nhs-outcomes-framework-indicators",
          "national-diabetes-audit-2020-21-type-1-diabetes"]:
    melt_count(p)
