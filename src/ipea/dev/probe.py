import sys; sys.path.insert(0, "src")
from subsets_utils import get
import json

def vals(code):
    r = get(f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{code}')", timeout=(10,120))
    r.raise_for_status()
    return r.json()["value"]

# macro annual
m = vals("ABATE_ABPEAV")
print("MACRO ABATE_ABPEAV rows:", len(m), "sample:", m[0])

# find a regional series and a monthly one from metadata
meta = get("http://www.ipeadata.gov.br/api/odata4/Metadados", timeout=(10,120)).json()["value"]
reg = [x for x in meta if x.get("BASNOME")=="Regional"][:5]
print("\nregional sample codes:", [(x["SERCODIGO"], x["PERNOME"]) for x in reg])
rv = vals(reg[0]["SERCODIGO"])
print("REGIONAL", reg[0]["SERCODIGO"], "rows:", len(rv), "sample:", rv[0] if rv else None)
# check NIVNOME/TERCODIGO populated
nonempty_ter = [x for x in rv if x.get("TERCODIGO")]
print("regional rows with TERCODIGO:", len(nonempty_ter), "of", len(rv))
