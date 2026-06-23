import sys
from utils import install_browser_client, yearbook_workbook_url, enforcement_workbook_url, download_workbook, parse_sheet
from constants import ENTITY_META

install_browser_client()
# cache workbooks by url
cache={}
def wb_for(meta):
    url = enforcement_workbook_url() if meta["section_kw"] is None else yearbook_workbook_url(meta["section_kw"])
    if url not in cache:
        cache[url]=download_workbook(url)
    return cache[url], url

bad=[]; thin=[]; ok=0
for eid,meta in ENTITY_META.items():
    try:
        content,url=wb_for(meta)
        names,rows=parse_sheet(content, meta["sheet"])
        n=len(rows)
        ncol=len(names)
        if n==0:
            bad.append((eid,meta["sheet"],"0 rows")); continue
        if n<3:
            thin.append((eid,meta["sheet"],n))
        ok+=1
        if eid in ("yearbook-lpr-table-1","enforcement-ero-arrests-by-citizenship","yearbook-lpr-table-2","enforcement-dhs-repats-by-type","yearbook-nonimmigrant-table-26"):
            print(f"\n# {eid}  rows={n} cols={ncol}: {names[:8]}")
            for r in rows[:3]: print("   ", {k:r[k] for k in list(r)[:6]})
    except Exception as e:
        bad.append((eid,meta["sheet"],f"{type(e).__name__}: {e}"))

print(f"\n=== ok={ok} thin={len(thin)} bad={len(bad)} of {len(ENTITY_META)} ===")
print("THIN:", thin)
print("BAD:")
for b in bad: print("  ",b)
