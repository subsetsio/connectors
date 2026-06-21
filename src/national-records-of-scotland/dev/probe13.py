import sys,time; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD

def phase1(ds, period, last, lim=50000):
    flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
    pf=f'; <{RP}> <{period}>' if period else ''
    return M._sparql(f'PREFIX qb: <{QB}> SELECT ?obs WHERE {{ ?obs qb:dataSet <{ds}>{pf} . {flt} }} ORDER BY ?obs LIMIT {lim}')

def phase2(obs_uris):
    vals=" ".join(f"<{u}>" for u in obs_uris)
    return M._sparql(f'SELECT ?obs ?p ?o WHERE {{ VALUES ?obs {{ {vals} }} ?obs ?p ?o }}')

# life-expectancy P3Y
ds=M.DATA_BASE+"Life-Expectancy"; pv=M._discover_periods(ds)[-1]
t=time.time(); obs=[r["obs"] for r in phase1(ds,pv,None)]; print(f"LE P3Y phase1: {len(obs)} obs {time.time()-t:.1f}s")
chunk=obs[:4000]
t=time.time(); tr=phase2(chunk); print(f"LE phase2 4000 obs -> {len(tr)} triples {time.time()-t:.1f}s")
# pivot one obs
from collections import defaultdict
g=defaultdict(dict)
for r in tr: g[r["obs"]][r["p"]]=r["o"]
import json; print("sample obs preds:", json.dumps(list(g[chunk[0]].keys()),indent=0))
print("sample obs vals:", g[chunk[0]])

# historical one year phase1 timing (big)
H=M.DATA_BASE+"population-estimates-historical-geographic-boundaries"; hy=M._discover_periods(H)[0]
t=time.time(); o2=phase1(H,hy,None); print(f"HIST {M._seg(hy)} phase1 page0: {len(o2)} {time.time()-t:.1f}s")
