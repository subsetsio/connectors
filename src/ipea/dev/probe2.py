import sys; sys.path.insert(0,"src")
from subsets_utils import get, transient_retry
meta = get("http://www.ipeadata.gov.br/api/odata4/Metadados", timeout=(10,120)).json()["value"]
@transient_retry()
def vals(code):
    r=get(f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')", timeout=(10,180))
    r.raise_for_status()
    return r.json()["value"]
import random
random.seed(2)
for base in ["Macroeconômico","Regional","Social"]:
    codes=[x["SERCODIGO"] for x in meta if x.get("BASNOME")==base]
    samp=random.sample(codes, 5)
    tot=0; mx=0; nullc=0; types=set(); nivs=set()
    for c in samp:
        v=vals(c)
        tot+=len(v); mx=max(mx,len(v))
        for r in v:
            vv=r["VALVALOR"]
            if vv is None: nullc+=1
            else: types.add(type(vv).__name__)
            nivs.add(r.get("NIVNOME"))
    print(f"{base}: 5 series total {tot} max {mx} null {nullc} types {types} nivs {sorted(str(x) for x in nivs)}")
