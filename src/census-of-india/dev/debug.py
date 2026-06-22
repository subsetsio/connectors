from utils import install_ca, _read_matrix, _find_marker, _to_number, _clean_text
from subsets_utils import get
from constants import ENTITY_FILES
install_ca()
# 1) PC11_A01 marker debug
u=ENTITY_FILES["PC11_A01"]["urls"][0]
g=_read_matrix(get(u,timeout=(10,180)).content, u)
print("PC11_A01 dims", len(g), "x", (len(g[0]) if g else 0))
mi,cols=_find_marker(g)
print("marker idx", mi, "ncols", (len(cols) if cols else None))
for i in range(min(6,len(g))):
    print(" row",i,[_clean_text(g[i][c])[:10] for c in range(min(12,len(g[i])))])
# 2) type inference debug for PC01_A01
u2=ENTITY_FILES["PC01_A01"]["urls"][0]
g2=_read_matrix(get(u2,timeout=(10,180)).content, u2)
mi2,cols2=_find_matrix2=_find_marker(g2)
data=g2[mi2+1:]
data=[r for r in data if not all(c>=len(r) or _clean_text(r[c])=="" for c in cols2)]
n=len(data)
print("\nPC01_A01 ncols",len(cols2),"datarows",n)
for c in cols2:
    nonblank=[r[c] for r in data if c<len(r) and _clean_text(r[c])!=""]
    num=sum(1 for v in nonblank if _to_number(v) is not None)
    sample=[_clean_text(v)[:10] for v in nonblank[:3]]
    print(f"  col{c}: nonblank={len(nonblank)}/{n} numeric={num} sample={sample}")
