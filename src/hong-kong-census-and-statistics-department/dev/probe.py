from subsets_utils import get
import csv, io, json

def comp(tb):
    r = get(f"https://www.censtatd.gov.hk/data/table_{tb}_comp.json", timeout=(10,60))
    r.raise_for_status()
    return r.json()

for tb in ["110-01001A", "310-31001", "210-06314"]:
    try:
        c = comp(tb)
    except Exception as e:
        print(tb, "COMP FAIL", type(e).__name__, e); continue
    theme = c.get("theme_id")
    comps = c.get("table_component_list") or []
    print(f"\n=== {tb}  theme_id={theme} since={c.get('since')} n_comp={len(comps)}")
    seen_cols=set()
    for cc in comps[:3]:
        sv, sp = cc.get("stat_var"), cc.get("stat_pres")
        url = f"https://www.censtatd.gov.hk/data/MDT_{theme}_{tb}_{sv}_{sp}.csv"
        rr = get(url, timeout=(10,60))
        ok = rr.status_code
        rows = list(csv.reader(io.StringIO(rr.text)))
        hdr = rows[0] if rows else []
        print(f"  {sv}/{sp} http={ok} nrows={len(rows)-1} cols={hdr} sample={rows[1] if len(rows)>1 else None}")
