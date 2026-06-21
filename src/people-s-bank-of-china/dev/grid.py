import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/[A-Za-z0-9_/]*?(?:attachDir|fileDir/resource/cms)/\d{4}/\d{2}/\d+\.(?:html?|xlsx?))', re.I)
def find(cat,want):
    html=get(cat,timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>',html,re.S|re.I):
        tm=re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>',tbl,re.S|re.I)
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if t.lower()==want.lower(): return DATA.findall(tbl)
    return []
def dec(raw):
    for e in ("gb18030","utf-8"):
        try:return raw.decode(e)
        except:continue
    return raw.decode("latin-1")
def cl(v):
    s="" if v is None else str(v)
    if s=="nan":s=""
    return re.sub(r"\s+"," ",s.replace("\xa0"," ").replace("　"," ")).strip()
for cat,want in [("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Official reserve assets"),
                 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242436/index.html","Corporate Goods Price Indices (CGPI)")]:
    links=find(cat,want); htm=[l for l in links if l.lower().endswith(('htm','html'))]
    print("\n#####",want, "links:",[l[-6:] for l in links])
    if not htm: continue
    text=dec(get(BASEH+htm[0],timeout=40).content)
    g=pd.read_html(io.StringIO(text))[0].map(cl).values.tolist()
    for i,row in enumerate(g[:10]):
        print(i,"|"," | ".join(row[:7]))
