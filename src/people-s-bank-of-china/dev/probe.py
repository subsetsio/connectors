import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/diaochatongjisi/(?:fileDir/resource/cms|attachDir)/\d{4}/\d{2}/\d+\.(?:htm|html|xls|xlsx))', re.I)

def find_link(cat_url, title_want):
    html = get(cat_url, timeout=40).text
    for tbl in re.findall(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>', html, re.S|re.I):
        tm = re.search(r'<td[^>]*align="left"[^>]*>(.*?)</td>', tbl, re.S|re.I)
        title = re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',tm.group(1))).strip() if tm else ''
        if title.lower()==title_want.lower():
            return DATA.findall(tbl), title
    return None, None

def decode(raw):
    for enc in ("gb18030","gbk","gb2312","utf-8"):
        try: return raw.decode(enc), enc
        except Exception: continue
    return raw.decode("latin-1"), "latin-1"

for cat_url, want in [
    ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Money Supply"),
    ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Depository Corporations Survey"),
]:
    links,title = find_link(cat_url, want)
    print("\n===========", want, "=>", links)
    htm = [l for l in links if l.lower().endswith(('.htm','.html'))][0]
    raw = get(BASEH+htm, timeout=40).content
    text,enc = decode(raw)
    print("decoded:",enc,"bytes:",len(raw))
    dfs = pd.read_html(io.StringIO(text))
    print("num tables:",len(dfs)," shapes:", [d.shape for d in dfs])
    df = dfs[0]
    print(df.head(30).to_string()[:2500])
