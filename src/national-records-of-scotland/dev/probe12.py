import sys,time; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M
ds=M.DATA_BASE+"Life-Expectancy"
dims=M._discover_dimensions(ds); period=M.REF_PERIOD
other=[(d,M._snake(M._seg(d))) for d in dims if d!=period]
pv=M._discover_periods(ds)[-1]
exp=M._count(ds,pv); print("expected",exp)

def q(order):
    lines=[f"?obs qb:dataSet <{ds}> ;", f"  <{period}> <{pv}> ;", "  qb:measureType ?mt ; ?mt ?value ."]
    sel=["?obs","?value","?mt"]
    for i,(uri,_) in enumerate(other):
        lines.append(f"  ?obs <{uri}> ?d{i} ."); sel.append(f"?d{i}")
    ob=" ORDER BY ?obs" if order else ""
    return f"PREFIX qb: <{M.QB}>\nSELECT {' '.join(sel)} WHERE {{\n"+"\n".join(lines)+f"\n}}{ob} LIMIT {M.PAGE}"

t=time.time(); rows=M._sparql(q(False)); print(f"NO order: n={len(rows)} {time.time()-t:.1f}s")
# also try a huge-year datazone dataset single-query no-order with sub-cap
