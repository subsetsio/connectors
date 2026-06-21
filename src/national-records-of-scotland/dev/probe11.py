import sys,time; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M
ds=M.DATA_BASE+"Life-Expectancy"
dims=M._discover_dimensions(ds)
period=M.REF_PERIOD
other=[(d,M._snake(M._seg(d))) for d in dims if d!=period]
print("other dims:",[c for _,c in other])
periods=M._discover_periods(ds)
print("n periods",len(periods))
pv=periods[-1]
exp=M._count(ds,pv)
print("year",M._seg(pv),"expected",exp)

# REQUIRED joins (no OPTIONAL), ORDER BY keyset
def page_required(last):
    lines=[f"?obs qb:dataSet <{ds}> ;", f"  <{period}> <{pv}> ;", "  qb:measureType ?mt ; ?mt ?value ."]
    sel=["?obs","?value","?mt"]
    for i,(uri,_) in enumerate(other):
        lines.append(f"  ?obs <{uri}> ?d{i} .")
        sel.append(f"?d{i}")
    if last:
        lines.append(f'FILTER(STR(?obs) > "{last}")')
    q=f"PREFIX qb: <{M.QB}>\nSELECT {' '.join(sel)} WHERE {{\n"+"\n".join(lines)+f"\n}} ORDER BY ?obs LIMIT {M.PAGE}"
    return q

last=None; tot=0
for i in range(6):
    t=time.time(); rows=M._sparql(page_required(last))
    print(f"page {i}: n={len(rows)} {time.time()-t:.1f}s")
    if not rows: break
    last=rows[-1]["obs"]; tot+=len(rows)
    if len(rows)<M.PAGE: break
print("year total",tot,"expected",exp)
