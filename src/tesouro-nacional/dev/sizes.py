import json
from subsets_utils import get
CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"
def res(slug):
    r = get(f"{CKAN}/package_show", params={"id": slug}, timeout=(10,120)); r.raise_for_status()
    return r.json()["result"]["resources"]
def sz(x):
    s = x.get("size")
    try: return int(s)
    except: return 0
for slug in ["operacoes-do-tesouro-direto","investidores-do-tesouro-direto","retencao-de-tributos-federais",
             "retencao-de-tributos-municipais","transferencias-constitucionais-para-estados",
             "transferencias-constitucionais-para-municipios","ds013","despesas-e-transferencias-totais"]:
    rs = res(slug)
    csv_sz = sum(sz(x) for x in rs if (x.get("format") or "").upper()=="CSV")
    xlsx_sz = sum(sz(x) for x in rs if (x.get("format") or "").upper() in {"XLSX","XLS"})
    ncsv = sum(1 for x in rs if (x.get("format") or "").upper()=="CSV")
    print(f"{slug}: {len(rs)} res, {ncsv} CSV; CSV={csv_sz/1e9:.2f}GB XLSX={xlsx_sz/1e6:.1f}MB")
    big = sorted(rs, key=lambda x:-sz(x))[:3]
    for x in big:
        print(f"    {x.get('format'):5} {sz(x):>14,}  {x.get('name','')[:45]!r}")
