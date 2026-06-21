import re, sys
from subsets_utils import get
sys.path.insert(0,"dev")
from parser import melt_workbook

def docurl(inst, did):
    return (f"https://www.statistics.gr/en/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_{inst}"
            f"&p_p_lifecycle=2&p_p_cacheability=cacheLevelPage"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_javax.faces.resource=document"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_ln=downloadResources"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_documentID={did}"
            f"&_documents_WAR_publicationsportlet_INSTANCE_{inst}_locale=en")

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
        r=get(u,timeout=(10,90)); ct=r.headers.get("content-type","")
        cd=r.headers.get("content-disposition","")
        fn=re.search(r'filename="?([^";]+)',cd); fn=fn.group(1).strip() if fn else did
        if any(x in ct for x in XL):
            out.append((fn,r.content))
    return out

for code in ["SDT03","SEL15","DKT87","SHE06","SPG06","DKT21"]:
    docs=excel_docs(code)
    total=0; sample=None
    for fn,content in docs:
        try:
            rows=melt_workbook(content,fn)
        except Exception as e:
            print(f"{code} {fn}: PARSE ERR {type(e).__name__} {e}"); continue
        total+=len(rows)
        if rows and sample is None: sample=rows[len(rows)//3]
    print(f"{code}: {len(docs)} excel file(s), {total} numeric rows; sample={sample}")
