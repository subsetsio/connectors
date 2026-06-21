import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB; RP=M.REF_PERIOD
def sp(query):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,300))
    return r.status_code, r.text
ds=M.DATA_BASE+"Life-Expectancy"; pv=M._discover_periods(ds)[-1]
print("pv=",pv)
q=f'PREFIX qb: <{QB}> SELECT ?obs ?p ?o WHERE {{ ?obs qb:dataSet <{ds}> ; <{RP}> <{pv}> . ?obs ?p ?o }} ORDER BY ?obs LIMIT 50000'
st,txt=sp(q); print("with ORDER:",st, txt[:200])
q2=f'PREFIX qb: <{QB}> SELECT ?obs ?p ?o WHERE {{ ?obs qb:dataSet <{ds}> ; <{RP}> <{pv}> . ?obs ?p ?o }} LIMIT 50000'
t=time.time(); st,txt=sp(q2); print("no ORDER:",st, "len",len(txt), f"{time.time()-t:.1f}s", "rows", txt.count(chr(10)))
