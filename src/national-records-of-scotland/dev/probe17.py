import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD
def sp(query):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,300))
    return r.status_code, list(csv.DictReader(io.StringIO(r.text))) if r.status_code==200 else r.text

def phase1(ds,period,last,lim=50000):
    flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
    st,rows=sp(f'PREFIX qb: <{QB}> SELECT ?obs WHERE {{ ?obs qb:dataSet <{ds}> ; <{RP}> <{period}> . {flt} }} ORDER BY ?obs LIMIT {lim}')
    return rows

def range_join(ds,period,other,lo,hi):
    lines=[f"?obs qb:dataSet <{ds}> ;", f"  <{RP}> <{period}> ;", "  qb:measureType ?mt ; ?mt ?value ."]
    sel=["?obs","?value","?mt"]
    for i,(uri,_) in enumerate(other):
        lines.append(f"  ?obs <{uri}> ?d{i} ."); sel.append(f"?d{i}")
    cond=f'STR(?obs) > "{lo}"' if lo else "true"
    lines.append(f'FILTER({cond} && STR(?obs) <= "{hi}")')
    return sp(f"PREFIX qb: <{QB}>\nSELECT {' '.join(sel)} WHERE {{\n"+"\n".join(lines)+"\n}")

for slug in ["Life-Expectancy","population-estimates-historical-geographic-boundaries"]:
    ds=M.DATA_BASE+slug
    dims=M._discover_dimensions(ds); other=[(d,M._snake(M._seg(d))) for d in dims if d!=RP]
    pv=M._discover_periods(ds)[0]
    obs=[r["obs"] for r in phase1(ds,pv,None)]
    print(f"\n{slug} {M._seg(pv)}: {len(obs)} obs (page0), dims={len(other)}")
    lo=None; hi=obs[min(4999,len(obs)-1)]
    t=time.time(); st,res=range_join(ds,pv,other,lo,hi)
    print(f"  range_join 5000: st={st} rows={len(res) if isinstance(res,list) else res} {time.time()-t:.1f}s")
    if isinstance(res,list) and res: print("  sample:",{k:res[0][k] for k in list(res[0])[:6]})
