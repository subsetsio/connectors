from subsets_utils import get
def fetch(url):
    r = get(url, timeout=90); return r.status_code, (r.json() if r.status_code==200 else r.text[:150])
def count_rows(data):
    n=0
    for res in data:
        for r in res["resultados"]:
            for s in r["series"]:
                n+=len(s["serie"])
    return n
# table with classification: IPCA15 1705, classif 315 (446 cats)
for aid, cids in [("1705",[315]), ("6579",[])]:
    sc, meta = fetch(f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/metadados")
    varids="|".join(str(v["id"]) for v in meta["variaveis"])
    level=next((L for L in ["N1","N2","N3"] if L in meta["nivelTerritorial"]["Administrativo"]), meta["nivelTerritorial"]["Administrativo"][0])
    cl="".join(f"&classificacao={c}[all]" for c in cids)
    url=f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/periodos/all/variaveis/{varids}?localidades={level}[all]{cl}"
    sc,data=fetch(url)
    print(f"{aid}: level={level} status={sc} n_var_results={len(data)} total_rows(N1,all-classif)={count_rows(data) if isinstance(data,list) else data}")
