import sys, os, re, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su
from utils import install_ca, parse_census_excel
install_ca()

_CODE_RE = re.compile(r"(^|_)(code|sl_no|s_no|sr_no|serial)(_|$)")

def classify(rows):
    cols = list(rows[0].keys())
    val_cols, id_cols = [], []
    for c in cols:
        vals = [r.get(c) for r in rows]
        nonnull = [v for v in vals if v is not None]
        numeric = nonnull and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in nonnull)
        if numeric and not _CODE_RE.search(c):
            val_cols.append(c)
        else:
            id_cols.append(c)
    return id_cols, val_cols

def melt(rows):
    id_cols, val_cols = classify(rows)
    region_col = id_cols[0] if id_cols else None
    out=[]
    for r in rows:
        dims = {c: r.get(c) for c in id_cols}
        region = r.get(region_col) if region_col else None
        for m in val_cols:
            v = r.get(m)
            if v is None: continue
            out.append({"region": region, "dimensions": json.dumps(dims, ensure_ascii=False), "measure": m, "value": float(v)})
    return id_cols, val_cols, out

cases = {
 "PC01_A02": "https://censusindia.gov.in/nada/index.php/catalog/20032/download/23164/PC01_A02.xls",
 "PC11_A02_india_xls": "https://censusindia.gov.in/nada/index.php/catalog/43333/download/47001/00%20A%202-India.xls",
 "PC11_A02_jk_xlsx": "https://censusindia.gov.in/nada/index.php/catalog/43334/download/47003/01%20A-2%20J%20%20K.xlsx",
 "PC11_A11_jk_xlsx": "https://censusindia.gov.in/nada/index.php/catalog/42944/download/46612/ST-0100-PCA-A-11-ddw.xlsx",
}
for name,url in cases.items():
    r = su.get(url, timeout=(10,120))
    rows = parse_census_excel(r.content, url)
    if not rows:
        print("===",name, r.status_code, "NO ROWS parsed"); continue
    id_cols, val_cols, out = melt(rows)
    print("===",name, r.status_code, "wide_rows",len(rows),"-> long",len(out))
    print("  id_cols:", id_cols)
    print("  val_cols:", val_cols)
    for row in out[:2]: print("   ", row)
