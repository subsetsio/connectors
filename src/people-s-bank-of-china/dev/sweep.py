import re, io, sys, time
sys.path.insert(0,"dev")
import pandas as pd
from subsets_utils import get
from parser import grid_from_htm, grid_from_xls, parse_grid, clean
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/[A-Za-z0-9_/]*?(?:attachDir|fileDir/resource/cms)/\d{4}/\d{2}/\d+\.(?:html?|xlsx?))', re.I)
def dec(raw):
    for e in ("gb18030","utf-8"):
        try:return raw.decode(e)
        except:continue
    return raw.decode("latin-1")
# 2024 category pages (id from nav)
CATS={
 "Aggregate Financing to the Real Economy":"5242421",
 "Money and Banking Statistics":"5242424",
 "Assets and Liabilities Statistics of Financial Institutions":"5242427",
 "Sources and Uses of Credit Funds of Financial Institutions":"5242430",
 "Financial Market Statistics":"5242433",
 "Corporate Goods Price Indices":"5242436",
}
# in-union titles to skip Financial Accounts (excluded)
total=0; bad=[]
for cat,cid in CATS.items():
    url=f"https://www.pbc.gov.cn/en/3688247/3688975/5242368/{cid}/index.html"
    html=get(url,timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>',html,re.S|re.I):
        tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
        title=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if not title: continue
        links=DATA.findall(tbl)
        htm=[l for l in links if l.lower().endswith(('htm','html'))]
        use = htm if htm else [l for l in links if l.lower().endswith(('xls','xlsx'))]
        if not use: bad.append((title,"NO DATA LINK")); continue
        try:
            raw=get(BASEH+use[0],timeout=40).content
            g = grid_from_htm(dec(raw)) if use[0].lower().endswith(('htm','html')) else grid_from_xls(raw)
            recs=parse_grid(g)
        except Exception as e:
            bad.append((title,f"ERR {type(e).__name__}: {e}")); continue
        n=len(recs); total+=1
        items=len(set(r['item'] for r in recs)); periods=len(set(r['period'] for r in recs))
        meas=len(set(r['measure'] for r in recs if r['measure']))
        flag = "  <-- ZERO" if n==0 else ""
        print(f"{n:5d} recs  items={items:3d} per={periods:2d} meas={meas} | {cat[:18]:18s} | {title[:48]}{flag}")
        time.sleep(0.2)
print("\nBAD:",bad)
