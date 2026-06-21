import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re, random
from subsets_utils import get

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ca-qc-isq/work/entity_union.json"))
ids = union if isinstance(union, list) else list(union.keys())
print("union size:", len(ids))
random.seed(7)
sample = random.sample(ids, 40)

def page_data(slug, lang):
    r = get(f"https://statistique.quebec.ca/{lang}/produit/tableau/{slug}", timeout=(10,40))
    if r.status_code != 200: return None, r.status_code
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    if not m: return None, "no_nextdata"
    return json.loads(m.group(1))["props"]["pageProps"]["data"], 200

from collections import Counter
c = Counter()
xlsx_ok = xlsx_404 = html_ok = 0
for slug in sample:
    data = st = None
    for lang in ("en","fr"):
        data, st = page_data(slug, lang)
        if data is not None: break
    if data is None:
        c["page_fail"] += 1; print(f"  PAGEFAIL {st} {slug[:50]}"); continue
    t = data.get("type"); c[t]+=1
    if t == "dynamique":
        url = f"https://statistique.quebec.ca/docs-ken/multimedia/Fichier_complet_{data['no']}.xlsx"
        h = get(url, timeout=(10,60))
        ok = h.status_code==200 and len(h.content)>500
        if ok: xlsx_ok+=1
        else: xlsx_404+=1
        print(f"  dyn  no={data['no']:>5} xlsx={h.status_code}/{len(h.content):>6}  {slug[:46]}")
    elif t == "statique":
        hh = data.get("html") or ""
        has = hh.count("<tr")>2
        if has: html_ok+=1
        print(f"  stat excel={str(data.get('excel'))[:24]:>24} html_tr={hh.count('<tr')}  {slug[:46]}")
    else:
        print(f"  ???  type={t} {slug[:46]}")

print("\ntype counts:", dict(c))
print(f"dynamic: xlsx_ok={xlsx_ok} xlsx_missing={xlsx_404}")
print(f"static: html_ok={html_ok}")
