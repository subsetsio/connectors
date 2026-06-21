from subsets_utils import get
PREF=["N3","N2","N1","N8","N9","N7","N6"]
def fetch(url):
    r=get(url,timeout=90); return r.status_code,(r.json() if r.status_code==200 else r.text[:120])
import json
u=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/ibge/work/entity_union.json"))
agg_ids=[x for x in u if x!="municipios"][:4]
for aid in agg_ids:
    sc,meta=fetch(f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/metadados")
    adm=meta["nivelTerritorial"]["Administrativo"]
    level=next((L for L in PREF if L in adm), adm[0] if adm else "N1")
    varids="|".join(str(v["id"]) for v in meta["variaveis"])
    url=f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/periodos/all/variaveis/{varids}?localidades={level}[all]"
    sc,data=fetch(url)
    rows=sum(len(s["serie"]) for res in data for r in res["resultados"] for s in r["series"]) if isinstance(data,list) else -1
    print(f"{aid} '{meta['nome'][:40]}' lvl={level} adm={adm} status={sc} rows={rows} freq={meta['periodicidade'].get('frequencia')}")
