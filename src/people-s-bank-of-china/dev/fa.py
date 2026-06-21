import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/[A-Za-z0-9_/]*?(?:attachDir|fileDir/resource/cms)/\d{4}/\d{2}/\d+\.(?:html?|xlsx?))', re.I)
def find(cat,want):
    html=get(cat,timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>',html,re.S|re.I):
        tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if t.lower()==want.lower(): return DATA.findall(tbl),t
    return [],None
def dec(raw):
    for e in ("gb18030","utf-8"):
        try:return raw.decode(e)
        except:continue
    return raw.decode("latin-1")
def cl(v):
    s="" if v is None else str(v)
    if s=="nan":s=""
    return re.sub(r"\s+"," ",s.replace("\xa0"," ").replace("　"," ")).strip()
# FA 2024 category 5647472
html=get("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5647472/index.html",timeout=40).text
for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>',html,re.S|re.I):
    tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
    t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
    print("TITLE:",repr(t),[l[-7:] for l in DATA.findall(tbl)])
links,t=find("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5647472/index.html","Flow of Funds Statement(Financial Accounts)(Year)")
print("\nlinks",links)
htm=[l for l in links if l.lower().endswith(('htm','html'))]
src = htm[0] if htm else (links[0] if links else None)
if src:
    raw=get(BASEH+src,timeout=40).content
    if src.lower().endswith(('htm','html')):
        g=pd.read_html(io.StringIO(dec(raw)))[0].map(cl).values.tolist()
    else:
        g=pd.read_excel(io.BytesIO(raw),header=None).map(cl).values.tolist()
    for i,row in enumerate(g[:10]): print(i,"|"," | ".join(row[:8]))
