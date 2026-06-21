import sys, os
sys.path.insert(0, os.path.abspath("src"))
from nodes.mhclg import (_sheets_for, _iter_cells, _get_json, _get_bytes,
                         CONTENT_API, _TABULAR_TYPES, BASE_PATHS)

for eid in [
  "government-statistics-english-indices-of-deprivation-2025",
  "government-statistical-data-sets-live-tables-on-homelessness",
]:
    bp = BASE_PATHS[eid]
    doc = _get_json(CONTENT_API+bp)
    atts = [a for a in (doc.get("details") or {}).get("attachments",[]) if a.get("content_type") in _TABULAR_TYPES]
    print("="*70, "\n", eid, "tabular attachments:", len(atts))
    total=0
    for a in atts[:2]:
        raw=_get_bytes(a["url"])
        sheets=_sheets_for(a["content_type"], raw)
        n=0; sample=None
        for sn,df in sheets:
            for cell in _iter_cells(a["filename"],a["title"],a["content_type"],df,str(sn)):
                n+=1
                if sample is None and cell[7] is not None: sample=cell
        total+=n
        print(f"  {a['filename']:<45} sheets={len(sheets):>2} cells={n}")
        if sample: print("     numeric sample: sheet=%s r%d c%d ="%(sample[3],sample[4],sample[5]), sample[6], "->", sample[7])
    print("  total cells (first 2 files):", total)
