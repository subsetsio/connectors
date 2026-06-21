import re, io, sys
sys.path.insert(0,"dev")
import pandas as pd
from subsets_utils import get
from parser import grid_from_htm, grid_from_xls, clean
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/[A-Za-z0-9_/]*?(?:attachDir|fileDir/resource/cms)/\d{4}/\d{2}/\d+\.(?:html?|xlsx?))', re.I)
def dec(raw):
    for e in ("gb18030","utf-8"):
        try:return raw.decode(e)
        except:continue
    return raw.decode("latin-1")
def links_for(cid,want):
    html=get(f"https://www.pbc.gov.cn/en/3688247/3688975/5242368/{cid}/index.html",timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>',html,re.S|re.I):
        tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if t.lower()==want.lower(): return DATA.findall(tbl)
    return []
for cid,want in [("5242427","Assets and Liabilities Statistics of Financial Institutions"),
                 ("5242424","Template on International Reserves and Foreign Currency Liquidity")]:
    links=links_for(cid,want)
    print("\n#####",want,"\n  links:",links)
    if not links: continue
    src=links[0]
    raw=get(BASEH+src,timeout=40).content
    g = grid_from_htm(dec(raw)) if src.lower().endswith(('htm','html')) else grid_from_xls(raw)
    print("  grid:",len(g),"x",len(g[0]) if g else 0)
    for i,row in enumerate(g[:14]): print("  ",i,"|"," | ".join(row[:8])[:160])
