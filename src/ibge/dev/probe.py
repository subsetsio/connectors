import json, gzip
from subsets_utils import get

def fetch(url):
    r = get(url, timeout=60)
    return r.status_code, r.json() if r.status_code==200 else r.text[:200]

# representative tables: monthly IPCA-15 variation(1705), pop estimate(6579),
# a PNAD continua annual, a census table. Probe metadata + data shape.
for aid in ["1705", "6579"]:
    sc, meta = fetch(f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/metadados")
    varids = [v["id"] for v in meta["variaveis"]]
    adm = meta["nivelTerritorial"]["Administrativo"]
    classif = [(c["id"], c["nome"], len(c.get("categorias",[]))) for c in meta.get("classificacoes",[])]
    print(f"\n=== {aid} {meta['nome'][:50]} ===")
    print("  levels:", adm, "| vars:", varids, "| classif:", classif, "| period:", meta["periodicidade"])
    # pick broadest level
    level = next((L for L in ["N1","N2","N3"] if L in adm), adm[0] if adm else "N1")
    varpath = "|".join(str(v) for v in varids)
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{aid}/periodos/all/variaveis/{varpath}?localidades={level}[all]"
    sc, data = fetch(url)
    print(f"  data level={level} status={sc} n_resultados={len(data) if isinstance(data,list) else 'ERR'}")
    if isinstance(data, list) and data:
        r0 = data[0]
        s0 = r0["resultados"][0]
        print("  result keys:", list(r0.keys()), "| classificacoes in result:", s0["classificacoes"])
        ser = s0["series"][0]
        print("  series[0] localidade:", ser["localidade"]["nome"], "| serie sample:", dict(list(ser["serie"].items())[:3]))
        print("  n_classif_combos(resultados):", len(r0["resultados"]))
