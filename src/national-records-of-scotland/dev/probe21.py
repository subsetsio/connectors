import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD; MT="http://purl.org/linked-data/cube#measureType"
def sp(query,t=180):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code,(list(csv.DictReader(io.StringIO(r.text))) if r.status_code==200 else r.text)
def paged(sel,where,t=180):
    out=[];last=None;pages=0
    while True:
        flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
        st,rows=sp(f'PREFIX qb: <{QB}> SELECT {sel} WHERE {{ {where} {flt} }} ORDER BY ?obs LIMIT 50000',t)
        if st!=200: raise RuntimeError(f"{st}:{rows[:80]}")
        if not rows: break
        out+=rows;last=rows[-1]["obs"];pages+=1
        if len(rows)<50000: break
    return out,pages
H=M.DATA_BASE+"population-estimates-historical-geographic-boundaries"
hp=M._discover_periods(H)
# count via POST
def count(ds,p):
    st,rows=sp(f'PREFIX qb: <{QB}> SELECT (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{ds}> ; <{RP}> <{p}> }}')
    return int(rows[0]["n"])
exp=count(H,hp[0])
t=time.time(); hv,pg=paged("?obs ?mt ?value", f"?obs qb:dataSet <{H}> ; <{RP}> <{hp[0]}> ; <{MT}> ?mt ; ?mt ?value .")
print(f"hist value col: {len(hv)} rows in {pg} pages, {time.time()-t:.1f}s, expected {exp}")
# dims for historical
print("hist dims:", [M._seg(d) for d in M._discover_dimensions(H)])
