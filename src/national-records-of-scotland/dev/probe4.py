from subsets_utils import get
import csv, io, time

SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query, t=180):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,t))
    r.raise_for_status()
    return r.text

# 1. the 0-observation dataset: check predicates / structure type
ds0="http://statistics.gov.scot/data/dwellings-by-council-tax-band-detailed-current-geographic-boundaries"
print("=== dwellings detailed: types of things in its graph ===")
print(q(f'''SELECT ?type (COUNT(*) AS ?n) WHERE {{
  ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type .
  ?s <http://purl.org/linked-data/cube#dataSet> <{ds0}> .
}} GROUP BY ?type'''))
print("--- any qb:dataSet links at all? distinct dataSet objects in its graph ---")
print(q(f'''SELECT ?ds (COUNT(*) AS ?n) WHERE {{
  GRAPH <http://statistics.gov.scot/graph/dwellings-by-council-tax-band-detailed-current-geographic-boundaries> {{ ?o <http://purl.org/linked-data/cube#dataSet> ?ds }}
}} GROUP BY ?ds'''))

# 2. direct cube CSV download endpoint test
print("\n=== try PublishMyData cube CSV download ===")
for url in [
  "https://statistics.gov.scot/data/births.csv",
  "https://statistics.gov.scot/downloads/cube?uri=http%3A%2F%2Fstatistics.gov.scot%2Fdata%2Fbirths",
]:
    try:
        r=get(url, timeout=(10,30))
        print(url, "->", r.status_code, "len", len(r.content), repr(r.text[:120]))
    except Exception as e:
        print(url, "ERR", e)

# 3. SPARQL OFFSET speed
print("\n=== OFFSET speed on births ===")
for off in [0, 800000]:
    t=time.time()
    txt=q(f'''PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?o WHERE {{ ?o qb:dataSet <http://statistics.gov.scot/data/births> }} ORDER BY ?o LIMIT 100000 OFFSET {off}''', t=300)
    print(f"offset {off}: {time.time()-t:.1f}s rows={txt.count(chr(10))}")
