from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"

def parse_page(d):
    ids=d["id"]; size=d["size"]; dim=d["dimension"]; value=d["value"]
    ndim=len(ids)
    strides=[1]*ndim
    for i in range(ndim-2,-1,-1):
        strides[i]=strides[i+1]*size[i+1]
    rd_pos=ids.index("reference_date")
    rd_stride=strides[rd_pos]
    date_index=dim["reference_date"]["category"]["index"]
    # position lookup per dim: category_id(int)->position
    pos={}
    for did in ids:
        if did=="reference_date": continue
        pos[did]={int(c):i for i,c in enumerate(dim[did]["category"]["index"])}
    getv = (lambda k: value.get(str(k))) if isinstance(value,dict) else (lambda k: value[k] if k<len(value) else None)
    rows=[]
    for s in d["extension"]["series"]:
        cats={int(dc["dimension_id"]):int(dc["category_id"]) for dc in s["dimension_category"]}
        base=0
        for did in ids:
            if did=="reference_date": continue
            base += pos[did][cats[int(did)]] * strides[ids.index(did)]
        for j,date in enumerate(date_index):
            v=getv(base + j*rd_stride)
            if v is None: continue
            rows.append((s["id"],s["label"],date,v))
    return rows

ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"
url=f"{BASE}/domains/3/datasets/{ds}/?lang=EN"
allrows=[]; p=1; nonnull_total=0
while True:
    d=get(url,params={"page":p,"page_size":100},timeout=(10,120)).json()
    n=len(d["extension"]["series"])
    if n==0: break
    v=d["value"]
    nonnull_total += (len([x for x in v.values() if x is not None]) if isinstance(v,dict) else len([x for x in v if x is not None]))
    allrows+=parse_page(d)
    if n<100: break
    p+=1
print("rows extracted:",len(allrows))
print("nonnull cells across pages:",nonnull_total)
print("distinct series:",len({r[0] for r in allrows}))
print("date range:",min(r[2] for r in allrows),"->",max(r[2] for r in allrows))
