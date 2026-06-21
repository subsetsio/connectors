import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from nodes.polymarket import _keyset_pages, _f, PRICE_HISTORY_MIN_VOLUME_USD
n_scope=0; n_total=0
for closed in ("false","true"):
    pages=0
    for rows in _keyset_pages("markets",{"closed":closed}):
        pages+=1; n_total+=len(rows)
        for m in rows:
            if (_f(m.get("volumeNum")) or 0)>=PRICE_HISTORY_MIN_VOLUME_USD:
                try:
                    oc=[str(o).strip().lower() for o in json.loads(m.get("outcomes") or "[]")]
                    tk=json.loads(m.get("clobTokenIds") or "[]")
                except Exception: continue
                if oc==["yes","no"] and tk: n_scope+=1
        if pages>=8: break  # sample only 8 pages per state
    print(f"closed={closed}: sampled {pages} pages")
print(f"sampled total rows={n_total}, scoped(>=100k binary)={n_scope}")
