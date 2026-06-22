from utils import install_ca, _read_matrix, _clean_text, _find_marker
from subsets_utils import get
from constants import ENTITY_FILES
import re
install_ca()
u=ENTITY_FILES["PC11_A01"]["urls"][0]
g=_read_matrix(get(u,timeout=(10,180)).content, u)
print("direct _find_marker:", _find_marker(g)[0])
# replicate logic for rows 0..5
for i,row in enumerate(g[:6]):
    seq=[]; ok=True
    for c,v in enumerate(row):
        s=_clean_text(v)
        if s=="": continue
        m=re.fullmatch(r"(\d+)(?:\.0+)?", s)
        if not m: ok=False; break
        seq.append((c,int(m.group(1))))
    print(f"row{i}: ok={ok} len={len(seq)} match={[n for _,n in seq]==list(range(1,len(seq)+1))} first={seq[:3]} brokenat={'' if ok else repr(_clean_text(row[c])[:20])}")
