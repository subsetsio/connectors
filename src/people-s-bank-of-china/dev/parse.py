import pandas as pd, re, io
from subsets_utils import get
BASEH="https://www.pbc.gov.cn"
DATA = re.compile(r'(/diaochatongjisi/(?:fileDir/resource/cms|attachDir)/\d{4}/\d{2}/\d+\.(?:htm|html|xls|xlsx))', re.I)
PERIOD = re.compile(r'^\s*(\d{4})[.\-/年]\s*(\d{1,2})\s*月?\s*$')
PERIOD_Q = re.compile(r'^\s*(\d{4})\s*$')  # year-only (annual)
NOTE = re.compile(r'^\s*(注|Note|注：|备注)', re.I)

def find_links(cat_url, want):
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
    s=str(v)
    if s=="nan": return ""
    s=s.replace("\xa0"," ").replace("　"," ")
    return re.sub(r"\s+"," ",s).strip()

def to_num(s):
    s=s.replace(",","").replace("%","").strip()
    if s in ("","-","—","…","..","/"): return None
    try: return float(s)
    except Exception: return None

def parse(text):
    df = pd.read_html(io.StringIO(text))[0]
    g = df.map(clean).values.tolist()
    nrows=len(g); ncols=len(g[0]) if g else 0
    # find header row = first row with >=2 period cells
    hdr=None; pcols={}
    for ri,row in enumerate(g):
        pc={ci:m for ci,c in enumerate(row) for m in [PERIOD.match(c)] if m}
        if len(pc)>=2:
            hdr=ri
            pcols={ci:(int(m.group(1)),int(m.group(2))) for ci,m in pc.items()}
            break
    if hdr is None: return [], "no monthly header"
    first_pcol=min(pcols)
    records=[]
    # collapse consecutive rows with identical value-vectors (bilingual stack)
    pending_label=[]; pending_vals=None
    def flush():
        nonlocal pending_label,pending_vals
        if pending_vals is not None and any(v is not None for _,v in pending_vals):
            label=" ".join(dict.fromkeys([x for x in pending_label if x]))
            for ci,v in pending_vals:
                if v is not None:
                    y,mo=pcols[ci]; records.append((label,f"{y}-{mo:02d}",v))
        pending_label=[]; pending_vals=None
    for ri in range(hdr+1,nrows):
        row=g[ri]
        joined=" ".join(c for c in row if c)
        if NOTE.match(joined): break
        lead=[row[ci] for ci in range(first_pcol) if ci<ncols]
        lead=[x for x in lead if x]
        vals=[(ci,to_num(row[ci])) for ci in pcols if ci<ncols]
        valtuple=tuple(v for _,v in vals)
        label=" ".join(dict.fromkeys(lead))
        if all(v is None for v in valtuple):
            continue
        if pending_vals is not None and valtuple==tuple(v for _,v in pending_vals):
            pending_label.extend(lead)  # same data, different-language label
        else:
            flush(); pending_label=list(lead); pending_vals=vals
    flush()
    return records, f"hdr@{hdr} pcols={len(pcols)} leadcols={first_pcol}"

CASES=[
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Money Supply"),
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Depository Corporations Survey"),
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242424/index.html","Official reserve assets"),
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242436/index.html","Corporate Goods Price Indices (CGPI)"),
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242421/index.html","Aggregate Financing to the Real Economy (Stock)"),
 ("https://www.pbc.gov.cn/en/3688247/3688975/5242368/5242433/index.html","Statistics of Shibor"),
]
for cat,want in CASES:
    links=find_links(cat,want)
    htm=[l for l in links if l.lower().endswith(('.htm','.html'))]
    if not htm: print(f"\n##### {want}: NO HTM links={links}"); continue
    text=decode(get(BASEH+htm[0],timeout=40).content)
    recs,info=parse(text)
    print(f"\n##### {want}: {info}  -> {len(recs)} records")
    for r in recs[:4]: print("   ",r)
    if recs: print("    ...last:",recs[-1])
