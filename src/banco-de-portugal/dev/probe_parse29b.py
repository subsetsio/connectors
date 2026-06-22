import sys; sys.path.insert(0,"src")
from subsets_utils import get
from nodes.banco_de_portugal import _parse_page
DS="23e0cdd56bddb4ad3016a9c3ad63a539"; DOM=29
def fetch(ps,page):
    r=get(f"https://bpstat.bportugal.pt/data/v1/domains/{DOM}/datasets/{DS}/",
          params={"lang":"EN","page":page,"page_size":ps},timeout=(10,180))
    r.raise_for_status(); return r.json()

def crawl(ps, maxpages):
    out={}
    page=1
    while page<=maxpages:
        d=fetch(ps,page)
        if not d["extension"]["series"]: break
        for sid,label,date,val in _parse_page(d):
            out[(sid,date)]=val
        n=len(d["extension"]["series"])
        if n<ps: break
        page+=1
    return out

a=crawl(1,12)     # ~12 series via ps=1
b=crawl(2,6)      # ~12 series via ps=2
c=crawl(100,1)    # 100 series via ps=100 single page
print("ps1 rows",len(a),"ps2 rows",len(b),"ps100 rows",len(c))
def cmp(x,y,nx,ny):
    inter=set(x)&set(y)
    bad=[(k,x[k],y[k]) for k in inter if x[k]!=y[k]]
    print(f"{nx} vs {ny}: intersection={len(inter)} mismatches={len(bad)}", bad[:3])
cmp(a,b,"ps1","ps2")
cmp(a,c,"ps1","ps100")
cmp(b,c,"ps2","ps100")
