from utils import install_ca, _read_matrix, _find_marker, _clean_text, _to_number, _NIL_TOKENS
from subsets_utils import get
from constants import ENTITY_FILES
install_ca()
u=ENTITY_FILES["PC01_A02"]["urls"][0]
g=_read_matrix(get(u,timeout=(10,180)).content, u)
mi,cols=_find_marker(g)
print("marker row", mi, "cols", cols)
data=[r for r in g[mi+1:] if not all(c>=len(r) or _clean_text(r[c])=="" for c in cols)]
n=len(data); print("datarows", n)
for c in cols:
    nb=[r[c] for r in data if c<len(r) and _clean_text(r[c])!=""]
    nums=sum(1 for v in nb if _to_number(v) is not None)
    nil=sum(1 for v in nb if _clean_text(v).lower() in _NIL_TOKENS)
    print(f" col{c}: nonblank={len(nb)}/{n} nums={nums} nil={nil} sample={[_clean_text(v)[:12] for v in nb[:4]]}")
