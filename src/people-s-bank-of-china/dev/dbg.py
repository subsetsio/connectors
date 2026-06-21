import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/diaochatongjisi/(?:fileDir/resource/cms|attachDir)/\d{4}/\d{2}/\d+\.(?:htm|html|xls|xlsx))', re.I)
def titles(cat_url):
    html=get(cat_url,timeout=40).text
    out=[]
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>', html, re.S|re.I):
        tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        out.append((t, [l[-5:] for l in DATA.findall(tbl)]))
    return out
print("== Financial Market Statistics 2024 ==")
for t,ext in titles("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242433/index.html"): print("  ",repr(t),ext)
print("== Corporate Goods Price Indices 2024 ==")
for t,ext in titles("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242436/index.html"): print("  ",repr(t),ext)
