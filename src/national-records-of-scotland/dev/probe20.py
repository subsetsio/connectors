import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD; MT="http://purl.org/linked-data/cube#measureType"
def sp(query,t=180):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code,(list(csv.DictReader(io.StringIO(r.text))) if r.status_code==200 else r.text)
def paged(sel,where,t=180):
    out=[];last=None
    while True:
        flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
        st,rows=sp(f'PREFIX qb: <{QB}> SELECT {sel} WHERE {{ {where} {flt} }} ORDER BY ?obs LIMIT 50000',t)
        if st!=200: raise RuntimeError(f"{st}:{rows[:80]}")
        if not rows: break
        out+=rows;last=rows[-1]["obs"]
        if len(rows)<50000: break
    return out

# LE full period assemble
ds=M.DATA_BASE+"Life-Expectancy"; dims=M._discover_dimensions(ds); pv=M._discover_periods(ds)[0]
other=[(d,M._snake(M._seg(d))) for d in dims if d!=RP]
vals=paged("?obs ?mt ?value", f"?obs qb:dataSet <{ds}> ; <{RP}> <{pv}> ; <{MT}> ?mt ; ?mt ?value .")
rowmap={r["obs"]:{"measure_type":M._seg(r["mt"]),"value":r["value"]} for r in vals}
for uri,col in other:
    dc=paged("?obs ?v", f"?obs qb:dataSet <{ds}> ; <{RP}> <{uri}> ?v .".replace(f"<{RP}> <{uri}>", f"<{RP}> <{pv}> ; <{uri}>"))
    for r in dc:
        if r["obs"] in rowmap: rowmap[r["obs"]][col]=M._seg(r["v"])
print("LE period rows:",len(rowmap),"expected",M._count(ds,pv))
print("sample:",list(rowmap.values())[0])

# historical: periods + one big period value col timing
H=M.DATA_BASE+"population-estimates-historical-geographic-boundaries"
t=time.time(); hp=M._discover_periods(H); print(f"hist periods: {len(hp)} {time.time()-t:.1f}s")
t=time.time(); hv=paged("?obs ?mt ?value", f"?obs qb:dataSet <{H}> ; <{RP}> <{hp[0]}> ; <{MT}> ?mt ; ?mt ?value .")
print(f"hist value col 1 period: {len(hv)} rows {time.time()-t:.1f}s expected {M._count(H,hp[0])}")
