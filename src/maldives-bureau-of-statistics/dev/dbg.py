import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re, importlib.util
import pandas as pd
spec=importlib.util.spec_from_file_location("p", os.path.join(os.path.dirname(__file__),"parse.py"))
P=importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
from subsets_utils import get
page=get("https://statisticsmaldives.gov.mv/yearbook/statisticalarchive/", timeout=(10,120)).text
hrefs={}
for m in re.finditer(r'href="([^"]+/(\d+\.\d+)\.xlsx?)"', page): hrefs.setdefault(m.group(2),m.group(1))
for tid in ["12.1","22.1"]:
    url=hrefs[tid]; ext=url.rsplit('.',1)[-1]
    df=pd.read_excel(io.BytesIO(get(url,timeout=(10,120)).content),header=None,engine=('openpyxl' if ext=='xlsx' else 'xlrd'))
    rows=df.values.tolist()
    def nn(r): return sum(0 if P._isnull(c) else 1 for c in r)
    s=0
    while s<len(rows) and nn(rows[s])<=1: s+=1
    block=rows[s:]; ncol=max(len(r) for r in block); block=[list(r)+[None]*(ncol-len(r)) for r in block]
    keep=[j for j in range(ncol) if any(not P._isnull(r[j]) for r in block)]
    block=[[r[j] for j in keep] for r in block]; ncol=len(keep)
    fr={j: round(sum(1 for r in block if not P._isnull(r[j]) and P._is_num(r[j]))/max(1,sum(1 for r in block if not P._isnull(r[j]))),2) for j in range(ncol)}
    print("="*50, tid, "ncol",ncol,"start_row",s)
    print("frac_num per col:", fr)
    with pd.option_context('display.max_columns',14,'display.width',200,'display.max_colwidth',22):
        print(pd.DataFrame(block).head(8).to_string())
