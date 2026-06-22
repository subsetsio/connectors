from subsets_utils import get
CKAN = "https://www.tesourotransparente.gov.br/ckan/api/3/action"
def csv_url(slug, pick=None):
    r = get(f"{CKAN}/package_show", params={"id": slug}, timeout=(10,120)); r.raise_for_status()
    rs = r.json()["result"]["resources"]
    cands = [x for x in rs if (x.get("format") or "").upper()=="CSV"]
    if pick: cands = [x for x in cands if pick in (x.get("name") or "")] or cands
    return cands[0]["url"]

for slug in ["vendas-do-tesouro-direto","transferencias-constitucionais-para-municipios","capag-estados"]:
    u = csv_url(slug)
    r = get(u, headers={"Range":"bytes=0-1500"}, timeout=(10,120))
    raw = r.content
    print("="*80); print(slug, "status", r.status_code, "len", len(raw))
    for enc in ("utf-8","latin-1"):
        try:
            txt = raw.decode(enc); print(f"  decode {enc} OK"); break
        except Exception as e:
            print(f"  decode {enc} FAIL {e}")
    print("  first 3 lines:")
    for line in txt.splitlines()[:3]:
        print("   |", line[:160])
