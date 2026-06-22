import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json
from subsets_utils import get
for id in (301, 1103):
    r = get(f"https://www.nsi.bg/opendata/getopendata_json.php?l=en&id={id}", timeout=(10,120))
    d = r.json()
    print("="*40, "id", id, "label=", d.get("label"))
    print("ids:", d["id"], "size:", d["size"], "role:", d.get("role"))
    dim = d["dimension"]
    for dk in d["id"]:
        cat = dim[dk]["category"]
        idx = cat.get("index"); lab = cat.get("label")
        print(f"  dim {dk!r} label={dim[dk].get('label')!r}")
        print("     index:", idx if not isinstance(idx,(list,dict)) or len(idx)<=6 else f'{type(idx).__name__} n={len(idx)}')
        print("     label:", (list(lab.items())[:6] if isinstance(lab,dict) else lab) if lab else None)
    print("value len:", len(d["value"]), "prod sizes:", __import__('math').prod(d["size"]))
    print("nulls in value:", sum(1 for v in d["value"] if v is None))
