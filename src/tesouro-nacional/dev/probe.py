import json
from subsets_utils import get

CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"

def pkg(slug):
    r = get(f"{CKAN}/package_show", params={"id": slug}, timeout=(10,120))
    r.raise_for_status()
    return r.json()["result"]

# Probe a few representative entity-union packages with varied resource counts
for slug in ["vendas-do-tesouro-direto", "api-rreo-entes", "estoque-da-divida-publica-federal",
             "capag-municipios", "transferencias-obrigatorias-da-uniao-por-municipio"]:
    p = pkg(slug)
    res = p.get("resources", [])
    print("="*80)
    print(f"{slug}  ({len(res)} resources)  org={p.get('organization',{}).get('name')}")
    fmts = {}
    for r in res:
        fmts[r.get("format","")] = fmts.get(r.get("format",""),0)+1
    print("  formats:", fmts)
    for r in res[:6]:
        print(f"   - [{r.get('format')}] name={r.get('name')!r} size={r.get('size')} url=...{r.get('url','')[-60:]}")
