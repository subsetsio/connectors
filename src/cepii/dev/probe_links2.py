import re
from subsets_utils import get

IDS = {
 "geodep":"41","geodist":"6","institutional-profiles":"ipd","language":"19",
 "product-level-trade-elasticities":"35","rprod":"40","tradhist":"32",
}
for ent, cid in IDS.items():
    url = "https://www.cepii.fr/IPD.asp" if cid == "ipd" else f"https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id={cid}"
    try:
        r = get(url, timeout=(10, 60)); r.raise_for_status(); html = r.text
    except Exception as e:
        print(f"\n### {ent} FETCH ERROR {e}"); continue
    # any download-ish href
    hrefs = re.findall(r'href=["\']?([^"\'> ]+)', html, re.I)
    dl = [h for h in hrefs if re.search(r'\.(zip|csv|xls|xlsx|dta|rds|7z|gz|tar|txt|sas7bdat)$', h, re.I)
          or 'DATA_DOWNLOAD' in h or 'download' in h.lower() or 'distance' in h.lower() or 'telech' in h.lower()]
    print(f"\n### {ent} ({cid})  candidates={len(set(dl))}")
    for h in sorted(set(dl))[:30]:
        print("   ", h)
