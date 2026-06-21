from subsets_utils import get
import csv, io, time
SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query, t=180):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code, r.text

QB='PREFIX qb: <http://purl.org/linked-data/cube#>'
B='http://statistics.gov.scot/data/births'

# re-verify empty dataset two ways
ds0="http://statistics.gov.scot/data/dwellings-by-council-tax-band-detailed-current-geographic-boundaries"
print("empty check count:", q(f'{QB} SELECT (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{ds0}> }}')[1].strip())
print("empty check sample:", q(f'{QB} SELECT ?o WHERE {{ ?o qb:dataSet <{ds0}> }} LIMIT 3')[1].strip())

# max limit test - no order
for lim in [50000, 100000, 200000]:
    t=time.time(); st,txt=q(f'{QB} SELECT ?o WHERE {{ ?o qb:dataSet <{B}> }} LIMIT {lim}', t=300)
    print(f"LIMIT {lim} (no order): status={st} rows={txt.count(chr(10))} {time.time()-t:.1f}s")

# distinct refPeriod for births
st,txt=q(f'{QB} SELECT DISTINCT ?p WHERE {{ ?o qb:dataSet <{B}> ; <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?p }} ORDER BY ?p')
yrs=[r["p"] for r in csv.DictReader(io.StringIO(txt))]
print("births distinct refPeriod:", len(yrs), yrs[:3], yrs[-2:])

# count obs for one year
y=yrs[-1]
st,txt=q(f'{QB} SELECT (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{B}> ; <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <{y}> }}')
print("births one-year count:", y, txt.strip())
