import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re
from subsets_utils import get

def page_data(slug, lang="en"):
    r = get(f"https://statistique.quebec.ca/{lang}/produit/tableau/{slug}", timeout=(10,60))
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
    d = json.loads(m.group(1))
    return d["props"]["pageProps"]["data"]

for slug, lang in [
    ("population-composantes-accroissement-demographique-trimestre-quebec","fr"),  # dynamique
    ("person-years-wage-bill-and-paid-hours-for-core-drilling-quebec","en"),       # statique
    ("gross-domestic-product-expenditure-quebec","en"),                            # dynamique, xlsx 404
]:
    d = page_data(slug, lang)
    h = d.get("html") or ""
    ntbl = h.count("<table")
    ntr = h.count("<tr")
    print(f"[{d.get('type'):>9}] no={d.get('no')} excel={d.get('excel')} | html_len={len(h)} <table>={ntbl} <tr>={ntr}  :: {slug[:40]}")
    # show first 220 chars of html
    print("    html head:", re.sub(r'\s+',' ', h[:220]))

# pls/ken fallback for GDP 4744
print("\n--- pls/ken header for 4744 (GDP) ---")
r = get("https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl=4744", timeout=(10,60))
print("header http", r.status_code, "len", len(r.text))
try:
    cfg = json.loads(r.text)
    ds = cfg.get("tableConfig",{}).get("dataSource",{})
    print("dataSource keys:", list(ds.keys()))
    print(json.dumps(ds, ensure_ascii=False)[:800])
except Exception as e:
    print("parse err", e, r.text[:300])
