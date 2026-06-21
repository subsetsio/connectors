import sys; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M

# small dataset
entity="household-type"
ds=M.DATA_BASE+entity
dims=M._discover_dimensions(ds)
period=next((d for d in dims if d==M.REF_PERIOD), None)
other=[(d,M._snake(M._seg(d))) for d in dims if d!=period]
print("dims:",dims)
print("period:",period)
print("other cols:",[c for _,c in other])
periods=M._discover_periods(ds)
print("n periods:",len(periods), periods[:2])
# one page of first period
pv=periods[0]
exp=M._count(ds,pv)
q=M._page_query(ds,period,pv,other,None)
rows=M._sparql(q)
print("period",M._seg(pv),"expected",exp,"got",len(rows))
# map a row
r=rows[0]
rec={"ref_period":M._seg(pv)}
for i,(_u,c) in enumerate(other): rec[c]=M._seg(r.get(f"d{i}"))
rec["measure_type"]=M._seg(r.get("mt")); rec["value"]=r.get("value")
print("sample rec:",rec)
print("ID_TO_ENTITY sample:", list(M.ID_TO_ENTITY.items())[:2])
print("n download specs:",len(M.DOWNLOAD_SPECS),"n transform:",len(M.TRANSFORM_SPECS))
