import re, io
from subsets_utils import get
import pandas as pd
PUB="https://www.statistics.gr/en/statistics/-/publication/{}/-"
LINK=re.compile(r'(https?://www\.statistics\.gr[^"]*?INSTANCE_[A-Za-z0-9]+[^"]*?documentID=\d+[^"]*?)"')
DID=re.compile(r'documentID=(\d+)')
XL=("officedocument.spreadsheetml","ms-excel")
def excel_docs(code):
    html=get(PUB.format(code),timeout=(10,60)).text
    out=[]; seen=set()
    for m in LINK.finditer(html):
        u=m.group(1).replace("&amp;","&"); did=DID.search(u).group(1)
        if did in seen: continue
        seen.add(did)
        r=get(u,timeout=(10,120)); ct=r.headers.get("content-type","").lower()
        cd=r.headers.get("content-disposition","")
        fn=re.search(r'filename="?([^";]+)',cd); fn=fn.group(1).strip() if fn else did
        if any(x in ct for x in XL): out.append((fn,r.content))
    return out
for code in ["SMA27","SME12","SME16"]:
    docs=excel_docs(code)
    print("="*60); print(code, "->", [fn for fn,_ in docs])
    for fn,content in docs[:1]:
        sheets=pd.read_excel(io.BytesIO(content),header=None,dtype=str,sheet_name=None)
        for sh,df in sheets.items():
            print(f"  sheet {sh!r} shape={df.shape}")
            g=df.where(pd.notna(df),None).values.tolist()
            for i,row in enumerate(g[:14]):
                print(f"   r{i}:", ["" if c is None else str(c)[:20] for c in row[:8]])
            break
