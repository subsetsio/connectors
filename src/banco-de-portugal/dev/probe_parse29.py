import sys; sys.path.insert(0,"src")
from subsets_utils import get
from nodes.banco_de_portugal import _parse_page

DS="23e0cdd56bddb4ad3016a9c3ad63a539"; DOM=29
def fetch(ps,page):
    r=get(f"https://bpstat.bportugal.pt/data/v1/domains/{DOM}/datasets/{DS}/",
          params={"lang":"EN","page":page,"page_size":ps},timeout=(10,180))
    r.raise_for_status(); return r.json()

# full reference at ps=100 (single page, all 4 series)
d100=fetch(100,1)
print("ps100 size",d100["size"],"value_len",len(d100["value"]) if isinstance(d100["value"],list) else "dict",
      "nseries",len(d100["extension"]["series"]))
ref={}
for sid,label,date,val in _parse_page(d100):
    ref[(sid,date)]=val
print("ps100 rows:",len(ref))

# paginated at ps=1
got={}
page=1
while True:
    d=fetch(1,page)
    ns=len(d["extension"]["series"])
    if ns==0: break
    if page==1:
        print("ps1 size",d["size"],"value_len",len(d["value"]) if isinstance(d["value"],list) else "dict","nseries",ns)
    for sid,label,date,val in _parse_page(d):
        got[(sid,date)]=val
    if ns<1: break
    page+=1
    if page>50: break
print("ps1 rows:",len(got))

# compare
print("keys match:", set(ref)==set(got))
mism=[(k,ref[k],got.get(k)) for k in ref if got.get(k)!=ref[k]]
print("value mismatches:",len(mism), mism[:3])
