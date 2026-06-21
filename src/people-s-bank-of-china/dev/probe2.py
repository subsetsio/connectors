import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/diaochatongjisi/(?:fileDir/resource/cms|attachDir)/\d{4}/\d{2}/\d+\.(?:htm|html|xls|xlsx))', re.I)
def find_link(cat_url, want):
    html = get(cat_url, timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>', html, re.S|re.I):
        tm = re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>', tbl, re.S|re.I)
        title = re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if title.lower()==want.lower(): return DATA.findall(tbl)
    return []
def decode(raw):
    for enc in ("gb18030","utf-8"):
        try: return raw.decode(enc)
        except Exception: continue
    return raw.decode("latin-1")
def clean(v):
    if v is None: return ""
    s=str(v); s=s.replace("\xa0"," ").replace("　"," ")
    return re.sub(r"\s+"," ",s).strip()
for want in ["Money Supply","Depository Corporations Survey"]:
    links=find_link("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html",want)
    htm=[l for l in links if l.lower().endswith(('.htm','.html'))][0]
    text=decode(get(BASEH+htm,timeout=40).content)
    df=pd.read_html(io.StringIO(text))[0]
    print("\n=====",want, df.shape)
    g=df.map(clean)
    for i,row in g.iterrows():
        cells=[c for c in row.tolist()]
        print(i,"|", " || ".join(cells[:9])[:200])
