import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from collections import defaultdict
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD; MT="http://purl.org/linked-data/cube#measureType"
def sp(query,t=120):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code, (list(csv.DictReader(io.StringIO(r.text))) if r.status_code==200 else r.text)

def paged(select_inner, t=120):
    """Page a query of form: ?obs <pattern> . returns list of dicts with ?obs first col."""
    out=[]; last=None
    while True:
        flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
        q=f'PREFIX qb: <{QB}> SELECT {select_inner[0]} WHERE {{ {select_inner[1]} {flt} }} ORDER BY ?obs LIMIT 50000'
        st,rows=sp(q,t)
        if st!=200: return None,st
        if not rows: break
        out+=rows; last=rows[-1]["obs"]
        if len(rows)<50000: break
    return out,200

ds=M.DATA_BASE+"Life-Expectancy"
pv=None
# discover dims + periods (retry a couple times for throttle)
for _ in range(4):
    dims=M._discover_dimensions(ds)
    if dims: break
    time.sleep(15)
print("dims:",len(dims), [M._seg(d) for d in dims])
periods=M._discover_periods(ds); print("periods:",len(periods))
pv=periods[0]
other=[(d,M._snake(M._seg(d))) for d in dims if d!=RP]

# value column for one period
t=time.time()
vals,st=paged((f"?obs ?mt ?value", f"?obs qb:dataSet <{ds}> ; <{RP}> <{pv}> ; <{MT}> ?mt ; ?mt ?value ."))
print(f"value col: {len(vals) if vals else st} rows {time.time()-t:.1f}s")
# one dimension column
d0uri=other[0][0]
t=time.time()
dc,st=paged((f"?obs ?v", f"?obs qb:dataSet <{ds}> ; <{RP}> <{pv}> ; <{d0uri}> ?v ."))
print(f"dim {other[0][1]}: {len(dc) if dc else st} rows {time.time()-t:.1f}s")
