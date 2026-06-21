from subsets_utils import get
import csv, io, time
SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query, t=240):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code, r.text
QB='PREFIX qb: <http://purl.org/linked-data/cube#>'
RP='<http://purl.org/linked-data/sdmx/2009/dimension#refPeriod>'
H='http://statistics.gov.scot/data/population-estimates-historical-geographic-boundaries'
y='http://reference.data.gov.uk/id/year/2001'

def page(last):
    flt=f'FILTER(STR(?obs) > "{last}")' if last else ''
    return q(f'{QB} SELECT ?obs WHERE {{ ?obs qb:dataSet <{H}> ; {RP} <{y}> . {flt} }} ORDER BY ?obs LIMIT 50000')

last=None; tot=0
for i in range(15):
    t=time.time(); st,txt=page(last)
    rows=[r["obs"] for r in csv.DictReader(io.StringIO(txt))]
    print(f"page {i}: st={st} n={len(rows)} {time.time()-t:.1f}s")
    if not rows: break
    last=rows[-1]; tot+=len(rows)
    if len(rows)<50000: break
print("total for year", tot, "expected 569043")
