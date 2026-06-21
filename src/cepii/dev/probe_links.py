import re
from subsets_utils import get

IDS = {
 "baci":"37","chelem":"17","econmap":"11","eqchange":"34","geodep":"41",
 "geodist":"6","gravity":"8","institutional-profiles":"ipd","intense":"43",
 "language":"19","macmap-hs6":"12","product-level-trade-elasticities":"35",
 "rprod":"40","trade-unit-values":"2","trade-volume":"42","tradeprod":"5",
 "tradhist":"32","world-trade-flows-characterization":"29",
}
for ent, cid in IDS.items():
    url = "https://www.cepii.fr/IPD.asp" if cid == "ipd" else f"https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id={cid}"
    try:
        r = get(url, timeout=(10, 60)); r.raise_for_status(); html = r.text
    except Exception as e:
        print(f"\n### {ent} ({cid}) FETCH ERROR {e}"); continue
    zips = set(re.findall(r'(/?DATA_DOWNLOAD/[^"\'> )]+\.zip)', html, re.I))
    zips |= set(re.findall(r'(https?://[^"\'> )]*DATA_DOWNLOAD/[^"\'> )]+\.zip)', html, re.I))
    print(f"\n### {ent} ({cid})  links={len(zips)}")
    for z in sorted(zips)[:25]:
        print("   ", z)
