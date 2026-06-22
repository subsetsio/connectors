import json
from subsets_utils import get
from collections import Counter

CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"
union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/tesouro-nacional/work/entity_union.json"))
ids = union if isinstance(union, list) else list(union.get("entities", union))
print("union size:", len(ids))

TAB = {"CSV","XLSX","XLS","ZIP","JSON","TSV","ODS"}
rows = []
for slug in ids:
    try:
        r = get(f"{CKAN}/package_show", params={"id": slug}, timeout=(10,120))
        r.raise_for_status()
        res = r.json()["result"].get("resources", [])
    except Exception as e:
        rows.append((slug, "ERR", str(e)[:40], 0)); continue
    fmts = Counter((x.get("format") or "?").upper() for x in res)
    tab_count = sum(c for f,c in fmts.items() if f in TAB)
    has_csv = fmts.get("CSV",0)
    has_xlsx = fmts.get("XLSX",0)+fmts.get("XLS",0)
    has_zip = fmts.get("ZIP",0)
    has_api = fmts.get("API",0)
    cls = "CSV" if has_csv else ("XLSX" if has_xlsx else ("ZIP" if has_zip else ("API" if has_api else "OTHER")))
    rows.append((slug, cls, dict(fmts), tab_count))

for slug, cls, fmts, n in sorted(rows, key=lambda r:r[1]):
    print(f"{cls:6} tab={n:3}  {slug:65} {fmts}")
print()
print("class counts:", Counter(r[1] for r in rows))
