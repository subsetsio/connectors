import math
from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"

def parse_page(d):
    ids=d["id"]; size=d["size"]; dim=d["dimension"]; value=d["value"]
    ndim=len(ids)
    strides=[1]*ndim
    for i in range(ndim-2,-1,-1):
        strides[i]=strides[i+1]*size[i+1]
    rd_pos=ids.index("reference_date")
    date_index=dim["reference_date"]["category"]["index"]
    # per non-date dim: position->category_id(int)
    catidx={did: dim[did]["category"]["index"] for did in ids if did!="reference_date"}
    # series lookup: frozenset((dim_id,cat_id))->(sid,label)
    slookup={}
    for s in d["extension"]["series"]:
        key=frozenset((int(dc["dimension_id"]),int(dc["category_id"])) for dc in s["dimension_category"])
        slookup[key]=(s["id"], s["label"])
    rows=[]
    miss=0
    items = value.items() if isinstance(value,dict) else enumerate(value)
    for flat,val in items:
        if val is None: continue
        idx=int(flat)
        coords={}
        for i,did in enumerate(ids):
            coords[did]= (idx//strides[i])%size[i]
        date=date_index[coords["reference_date"]]
        key=frozenset((int(did),int(catidx[did][coords[did]])) for did in ids if did!="reference_date")
        s=slookup.get(key)
        if s is None:
            miss+=1; continue
        rows.append((s[0],s[1],date,val))
    return rows,miss

ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"
url=f"{BASE}/domains/3/datasets/{ds}/?lang=EN"
allrows=[]; tot_miss=0; p=1
while True:
    d=get(url,params={"page":p,"page_size":100},timeout=(10,120)).json()
    n=len(d["extension"]["series"])
    if n==0: break
    rows,miss=parse_page(d)
    allrows+=rows; tot_miss+=miss
    if n<100: break
    p+=1
print("total rows:",len(allrows),"misses:",tot_miss)
print("distinct series:",len({r[0] for r in allrows}),"expected 917")
print("sample rows:")
for r in allrows[:4]: print("  ",r)
print("date range:",min(r[2] for r in allrows),"->",max(r[2] for r in allrows))
