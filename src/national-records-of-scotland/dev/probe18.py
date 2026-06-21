import sys,time; sys.path.insert(0,'src')
from subsets_utils import post
import csv,io
from nodes import national_records_of_scotland as M
QB=M.QB
def sp(query):
    r=post("https://statistics.gov.scot/sparql", data={"query":query}, headers={"Accept":"text/csv"}, timeout=(10,120))
    return r.status_code, list(csv.DictReader(io.StringIO(r.text))) if r.status_code==200 else r.text
ds=M.DATA_BASE+"Life-Expectancy"
print("DSD dims:", M._discover_dimensions(ds))
# actual predicates on a few LE observations
st,rows=sp(f'PREFIX qb: <{QB}> SELECT ?obs ?p WHERE {{ ?obs qb:dataSet <{ds}> ; ?p ?v }} LIMIT 60')
from collections import Counter
preds=Counter(r["p"] for r in rows)
for p,c in preds.items(): print(c,p)
