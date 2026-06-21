import json
from subsets_utils import get

def show(code):
    r = get(f"https://api.db.nomics.world/v22/series/ISM/{code}?observations=1", timeout=(10,120))
    r.raise_for_status()
    d = r.json()
    s = d["series"]
    print(f"=== {code}: num_found={s['num_found']} docs={len(s['docs'])}")
    doc = s["docs"][0]
    print("  doc keys:", sorted(doc.keys()))
    for sd in s["docs"]:
        per = sd.get("period", [])
        val = sd.get("value", [])
        print(f"  series_code={sd.get('series_code')!r} name={sd.get('series_name')!r} "
              f"dims={sd.get('dimensions')} nobs={len(per)} "
              f"first={per[0] if per else None}->{val[0] if val else None} "
              f"last={per[-1] if per else None}->{val[-1] if val else None}")
        print("    val types:", set(type(v).__name__ for v in val[:50]))

for c in ("pmi","prices","nm-pmi"):
    show(c)
