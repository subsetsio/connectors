import sys, os, re, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import subsets_utils as su
from utils import install_ca, parse_census_excel
install_ca()

_ID_NAME_RE = re.compile(r"(^|_)(code|sl_no|s_no|sr_no|serial|year|decade|t_r_u|tru|name|table_name)(_|$)")
_HAS_LETTER = re.compile(r"[A-Za-z]")

def is_value_col(c, rows):
    nonnull=[r.get(c) for r in rows if r.get(c) is not None]
    numeric = nonnull and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in nonnull)
    return numeric and not _ID_NAME_RE.search(c)

def excel_to_long(rows):
    cols=list(rows[0].keys())
    val_cols=[c for c in cols if is_value_col(c,rows)]
    id_cols=[c for c in cols if c not in val_cols]
    # region = first id col whose values mostly contain letters
    region_col=None
    for c in id_cols:
        sample=[str(r.get(c)) for r in rows[:30] if r.get(c) is not None]
        if sample and sum(1 for v in sample if _HAS_LETTER.search(v))>=0.6*len(sample):
            region_col=c; break
    if region_col is None and id_cols: region_col=id_cols[0]
    out=[]
    for r in rows:
        dims={c:r.get(c) for c in id_cols}
        region=r.get(region_col) if region_col else None
        for m in val_cols:
            v=r.get(m)
            if v is None: continue
            out.append({"region":region,"dimensions":json.dumps(dims,ensure_ascii=False),"measure":m,"value":float(v)})
    return id_cols,val_cols,region_col,out

cases={
 "PC11_A02_india": "https://censusindia.gov.in/nada/index.php/catalog/43333/download/47001/00%20A%202-India.xls",
 "PC11_A02_jk": "https://censusindia.gov.in/nada/index.php/catalog/43334/download/47003/01%20A-2%20J%20%20K.xlsx",
}
for name,url in cases.items():
    r=su.get(url,timeout=(10,120))
    rows=parse_census_excel(r.content,url)
    id_cols,val_cols,region_col,out=excel_to_long(rows)
    print("===",name,"region_col=",region_col)
    print("  val_cols:",val_cols)
    for row in out[:3]: print("   ",row)
