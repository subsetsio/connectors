from subsets_utils import get
import csv, io

SPARQL = "https://statistics.gov.scot/sparql.csv"

def q(query):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,120))
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))

ds = "http://statistics.gov.scot/data/births"

# 1. structure / components
print("=== predicates on one observation ===")
rows = q(f'''
SELECT ?p ?o WHERE {{
  ?obs <http://purl.org/linked-data/cube#dataSet> <{ds}> .
  ?obs ?p ?o .
}} LIMIT 25
''')
for r in rows:
    print(r["p"], "=>", r["o"])
