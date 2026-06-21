import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re, random
from subsets_utils import get

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ca-qc-isq/work/entity_union.json"))
ids = union if isinstance(union, list) else list(union.keys())
random.seed(11)
sample = random.sample(ids, 30)

def page_data(slug):
    for lang in ("en","fr"):
        r = get(f"https://statistique.quebec.ca/{lang}/produit/tableau/{slug}", timeout=(10,40))
        if r.status_code==200:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
            if m: return json.loads(m.group(1))["props"]["pageProps"]["data"], lang
    return None, None

def xlsx_variant(no):
    cands = [
        f"fichier_complet_{no}_eng.xlsx", f"Fichier_complet_{no}_eng.xlsx",
        f"fichier_complet_{no}.xlsx", f"Fichier_complet_{no}.xlsx",
    ]
    for name in cands:
        u = f"https://statistique.quebec.ca/docs-ken/multimedia/{name}"
        h = get(u, timeout=(10,60))
        if h.status_code==200 and len(h.content)>800:
            return name, len(h.content)
    return None, 0

dyn=dyn_xlsx_ok=0; stat=0; fails=0
for slug in sample:
    d,lang = page_data(slug)
    if d is None: fails+=1; print("PAGEFAIL", slug[:50]); continue
    t=d.get("type")
    if t=="dynamique":
        dyn+=1
        name,sz = xlsx_variant(d["no"])
        if name: dyn_xlsx_ok+=1
        print(f"  dyn no={d['no']:>5} xlsx={name or 'NONE':>32} sz={sz:>7} {slug[:34]}")
    elif t=="statique":
        stat+=1
        print(f"  stat html_tr={(d.get('html') or '').count('<tr'):>3} excel={str(d.get('excel'))[:18]:>18} {slug[:34]}")
print(f"\ndynamic={dyn} dyn_xlsx_ok={dyn_xlsx_ok}  static={stat}  pagefail={fails}")
