import re
from subsets_utils import get
html=get("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242433/index.html",timeout=40).text
for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>', html, re.S|re.I):
    tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
    t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
    if t=="Statistics of Shibor":
        print(tbl[:1500]); break
