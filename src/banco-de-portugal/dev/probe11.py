from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"
url=f"{BASE}/domains/3/datasets/{ds}/?lang=EN"
d=get(url,params={"page":1,"page_size":100},timeout=(10,120)).json()
ids=d["id"]; size=d["size"]; dim=d["dimension"]; value=d["value"]
ndim=len(ids)
strides=[1]*ndim
for i in range(ndim-2,-1,-1): strides[i]=strides[i+1]*size[i+1]
# collect all flat indices each series claims
claimed=set()
pos={did:{int(c):i for i,c in enumerate(dim[did]["category"]["index"])} for did in ids if did!="reference_date"}
ndates=size[ids.index("reference_date")]; rd_stride=strides[ids.index("reference_date")]
for s in d["extension"]["series"]:
    cats={int(dc["dimension_id"]):int(dc["category_id"]) for dc in s["dimension_category"]}
    base=sum(pos[did][cats[int(did)]]*strides[i] for i,did in enumerate(ids) if did!="reference_date")
    for j in range(ndates): claimed.add(base+j*rd_stride)
nonnull={int(k) for k,v in value.items() if v is not None}
unmatched=nonnull-claimed
print("page1 series:",len(d["extension"]["series"]),"nonnull:",len(nonnull),"claimed:",len(claimed),"unmatched:",len(unmatched))
# decode a few unmatched into per-dim categories
for idx in list(unmatched)[:3]:
    coords={did:(idx//strides[i])%size[i] for i,did in enumerate(ids)}
    decoded={}
    for i,did in enumerate(ids):
        if did=="reference_date":
            decoded["date"]=dim["reference_date"]["category"]["index"][coords[did]]
        else:
            decoded[did]=dim[did]["category"]["index"][coords[did]]
    print("unmatched",idx,decoded)
# does any series have dimension_category missing a dim?
ndims_nondate=[did for did in ids if did!="reference_date"]
for s in d["extension"]["series"][:0]: pass
sizes_dc=[len(s["dimension_category"]) for s in d["extension"]["series"]]
print("non-date dims:",len(ndims_nondate),"dim_category counts min/max:",min(sizes_dc),max(sizes_dc))
