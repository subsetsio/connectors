from utils import install_ca, _read_matrix, _clean_text
from subsets_utils import get
from constants import ENTITY_FILES
install_ca()
u=ENTITY_FILES["PC11_A01"]["urls"][0]
g=_read_matrix(get(u,timeout=(10,180)).content, u)
row=g[3]
vals=[_clean_text(v) for v in row]
print("row3 len", len(vals))
# find non-integer / gaps
import re
seq=[]
for c,s in enumerate(vals):
    if s=="": 
        seq.append((c,"BLANK")); continue
    m=re.fullmatch(r"(\d+)(?:\.0+)?", s)
    seq.append((c, int(m.group(1)) if m else f"NONINT:{s[:8]}"))
# print any that are not the expected value
print([x for x in seq if x[1]=="BLANK" or (isinstance(x[1],str) and x[1].startswith("NONINT"))][:20])
print("last 5:", seq[-5:])
