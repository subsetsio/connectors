import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, re, zipfile
import pandas as pd
from subsets_utils import get

LISTING = "https://www.customs.go.jp/kobe/boueki/02kakutei.html"

def listing():
    r = get(LISTING, timeout=(10,60)); r.raise_for_status()
    html = r.content.decode("shift_jis", "replace")
    pat = re.compile(r'(kakutei/r\d{2}/(\d{4})_(kakukaku|kaku)_([a-z_]+)\.zip)')
    rows = [(m[0], int(m[1]), m[2], m[3]) for m in pat.findall(html)]
    return rows

def melt_sheet(df, sheet):
    import numbers
    nrows, ncols = df.shape
    def isnum(v):
        return isinstance(v, numbers.Number) and not isinstance(v, bool) and pd.notna(v)
    # numeric cell positions
    numcells = [(r,c) for r in range(nrows) for c in range(ncols) if isnum(df.iat[r,c])]
    if not numcells: return []
    minr = min(r for r,_ in numcells); minc = min(c for _,c in numcells)
    # label columns = columns left of minc (text)
    label_cols = list(range(0, minc)) if minc>0 else [0]
    # header rows = rows above minr
    header_rows = list(range(0, minr)) if minr>0 else []
    # ffill label cols down
    lab = {}
    for c in label_cols:
        last=""
        for r in range(nrows):
            v=df.iat[r,c]
            if isinstance(v,str) and v.strip(): last=v.strip()
            lab[(r,c)]=last
    # ffill header rows right
    hdr={}
    for r in header_rows:
        last=""
        for c in range(ncols):
            v=df.iat[r,c]
            if isinstance(v,str) and v.strip(): last=v.strip()
            hdr[(r,c)]=last
    out=[]
    for r,c in numcells:
        rl=" ".join(x for x in (lab.get((r,cc),"") for cc in label_cols) if x)
        ch=" | ".join(x for x in (hdr.get((rr,c),"") for rr in header_rows) if x)
        out.append((sheet, rl, ch, r, c, float(df.iat[r,c])))
    return out

rows = listing()
bytype={}
for href,y,cls,t in rows: bytype.setdefault(t,[]).append((y,cls,href))
print("types:", sorted(bytype))
for t in ["shina_ex","kenbetsu","hyogo","kobe"]:
    # pick latest year, prefer kakukaku
    items=sorted(bytype[t])
    y,cls,href=items[-1]
    url="https://www.customs.go.jp/kobe/boueki/"+href
    r=get(url,timeout=(10,120)); r.raise_for_status()
    z=zipfile.ZipFile(io.BytesIO(r.content))
    inner=[n for n in z.namelist() if n.lower().endswith(('.xls','.xlsx'))][0]
    data=z.read(inner)
    sheets=pd.read_excel(io.BytesIO(data),sheet_name=None,header=None,engine='xlrd')
    total=0; samp=[]
    for sn,df in sheets.items():
        m=melt_sheet(df,sn); total+=len(m)
        if len(samp)<4 and m: samp.extend(m[:2])
    print(f"\n### {t} {y} {cls}: {len(sheets)} sheets, {total} numeric cells")
    for s in samp[:6]:
        print("   ", (s[0], s[1][:24], s[2][:30], "r%d c%d"%(s[3],s[4]), round(s[5],3)))
