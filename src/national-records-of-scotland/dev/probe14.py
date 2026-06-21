import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD

def sparql_post(query):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,300))
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))

def phase1(ds, period, last, lim=50000):
    flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
    return sparql_post(f'PREFIX qb: <{QB}> SELECT ?obs WHERE {{ ?obs qb:dataSet <{ds}> ; <{RP}> <{period}> . {flt} }} ORDER BY ?obs LIMIT {lim}')

def phase2(obs_uris):
    vals=" ".join(f"<{u}>" for u in obs_uris)
    return sparql_post(f'SELECT ?obs ?p ?o WHERE {{ VALUES ?obs {{ {vals} }} ?obs ?p ?o }}')

ds=M.DATA_BASE+"Life-Expectancy"; pv=M._discover_periods(ds)[-1]
t=time.time(); obs=[r["obs"] for r in phase1(ds,pv,None)]; print(f"LE phase1: {len(obs)} obs {time.time()-t:.1f}s")
t=time.time(); tr=phase2(obs[:5000]); print(f"LE phase2 5000obs -> {len(tr)} triples {time.time()-t:.1f}s")

# big year phase2 chunk on historical
H=M.DATA_BASE+"population-estimates-historical-geographic-boundaries"; hy=M._discover_periods(H)[0]
t=time.time(); o2=[r["obs"] for r in phase1(H,hy,None)]; print(f"HIST phase1 page0: {len(o2)} {time.time()-t:.1f}s")
t=time.time(); tr2=phase2(o2[:5000]); print(f"HIST phase2 5000obs -> {len(tr2)} triples {time.time()-t:.1f}s")
