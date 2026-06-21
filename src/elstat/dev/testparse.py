import re, sys
from subsets_utils import get
sys.path.insert(0,"dev")
from parser import melt_workbook, select_excel
from collections import Counter

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
        r=get(u,timeout=(10,120)); ct=r.headers.get("content-type","")
        cd=r.headers.get("content-disposition","")
        fn=re.search(r'filename="?([^";]+)',cd); fn=fn.group(1).strip() if fn else did
        if any(x in ct for x in XL):
            out.append((fn,r.content))
    return out

for code in ["SDT03","SEL15","DKT87","SHE06","SPG06","DKT21","SPK33","SJU06"]:
    try:
        docs=excel_docs(code)
    except Exception as e:
        print(f"{code}: FETCH ERR {e}"); continue
    sel=select_excel(docs)
    total=0; nanc=0; colgeneric=0; samples=[]
    for fn,content in sel:
        rows=melt_workbook(content,fn)
        total+=len(rows)
        nanc+=sum(1 for r in rows if r['value']!=r['value'])
        colgeneric+=sum(1 for r in rows if r['col_label'].startswith('col'))
        if rows: samples.append((fn, rows[len(rows)//2]))
    print(f"{code}: {len(docs)}->{len(sel)} files, {total} rows, nan={nanc}, genericcol={colgeneric}")
    for fn,s in samples[:1]:
        print(f"    {fn}: rl={s['row_label'][:30]!r} cl={s['col_label'][:30]!r} v={s['value']}")
