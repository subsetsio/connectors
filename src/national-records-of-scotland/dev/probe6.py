from subsets_utils import get
import csv, io, time
SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query, t=240):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    return r.status_code, r.text
QB='PREFIX qb: <http://purl.org/linked-data/cube#>'
RP='<http://purl.org/linked-data/sdmx/2009/dimension#refPeriod>'

# ORDER BY + LIMIT 50000 + OFFSET on a year subset
B='http://statistics.gov.scot/data/births'
t=time.time(); st,txt=q(f'{QB} SELECT ?o WHERE {{ ?o qb:dataSet <{B}> }} ORDER BY ?o LIMIT 50000 OFFSET 0')
print("ORDER BY L50000 O0:", st, txt.count(chr(10)), f"{time.time()-t:.1f}s")

# biggest dataset: per-year max count
H='http://statistics.gov.scot/data/population-estimates-historical-geographic-boundaries'
st,txt=q(f'{QB} SELECT ?p (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{H}> ; {RP} ?p }} GROUP BY ?p ORDER BY DESC(?n) LIMIT 3', t=240)
print("hist pop top years:\n", txt.strip())

# full sample observation row with dynamic dims for births one year, ORDER + offset works inside year
y='http://reference.data.gov.uk/id/year/2024'
qy=f'''{QB} SELECT ?obs ?refArea ?gender ?value
WHERE {{ ?obs qb:dataSet <{B}> ; {RP} <{y}> ;
  <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?refArea ;
  <http://statistics.gov.scot/def/dimension/gender> ?gender ;
  qb:measureType ?mt ; ?mt ?value . }}
ORDER BY ?obs LIMIT 50000 OFFSET 0'''
st,txt=q(qy)
rows=list(csv.DictReader(io.StringIO(txt)))
print("sample query status",st,"rows",len(rows))
print(rows[0] if rows else "none")
