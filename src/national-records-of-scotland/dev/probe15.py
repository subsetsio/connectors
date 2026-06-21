import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD
def sp(query):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,300))
    r.raise_for_status(); return list(csv.DictReader(io.StringIO(r.text)))
def eav(ds,period,last,lim=50000):
    flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
    return sp(f'PREFIX qb: <{QB}> SELECT ?obs ?p ?o WHERE {{ ?obs qb:dataSet <{ds}> ; <{RP}> <{period}> . {flt} ?obs ?p ?o }} ORDER BY ?obs LIMIT {lim}')

ds=M.DATA_BASE+"Life-Expectancy"; pv=M._discover_periods(ds)[-1]
t=time.time(); rows=eav(ds,pv,None); 
nobs=len(set(r["obs"] for r in rows))
print(f"LE P3Y EAV page0: {len(rows)} triples, {nobs} obs, {time.time()-t:.1f}s")

H=M.DATA_BASE+"population-estimates-historical-geographic-boundaries"; hy=M._discover_periods(H)[0]
t=time.time(); rows2=eav(H,hy,None)
print(f"HIST {M._seg(hy)} EAV page0: {len(rows2)} triples, {len(set(r['obs'] for r in rows2))} obs, {time.time()-t:.1f}s")
