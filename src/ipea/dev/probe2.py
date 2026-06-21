import sys; sys.path.insert(0,"src")
from subsets_utils import get
meta = get("http://www.ipeadata.gov.br/api/odata4/Metadados", timeout=(10,120)).json()["value"]
def vals(code):
    return get(f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')", timeout=(10,180)).json()["value"]
import random
random.seed(1)
# sample across bases
for base in ["Macroeconômico","Regional","Social"]:
    codes=[x["SERCODIGO"] for x in meta if x.get("BASNOME")==base]
    samp=random.sample(codes, 8)
    tot=0; mx=0; nullc=0; types=set(); nivs=set()
    for c in samp:
        v=vals(c)
        tot+=len(v); mx=max(mx,len(v))
        for r in v:
            vv=r["VALVALOR"]
            if vv is None: nullc+=1
            else: types.add(type(vv).__name__)
            nivs.add(r.get("NIVNOME"))
    print(f"{base}: 8 series, total {tot} rows, max {mx}, null VALVALOR {nullc}, types {types}, nivnomes {nivs}")
