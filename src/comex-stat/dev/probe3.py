from utils import ensure_ca
from subsets_utils import get
ensure_ca()
# bulk host (incomplete chain)
r = get("https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv", timeout=(10,60))
print("bulk", r.status_code, len(r.content))
# api host (cloudflare)
r2 = get("https://api-comexstat.mdic.gov.br/general/dates/updated", timeout=(10,60))
print("api", r2.status_code, r2.json()["data"])
