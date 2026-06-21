from subsets_utils import get
import csv, io, json

SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,180))
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))

eu = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/national-records-of-scotland/work/entity_union.json"))
ids = eu if isinstance(eu, list) else eu.get("entities") or list(eu.keys())
print("n entities:", len(ids))
total=0
for eid in ids:
    ds=f"http://statistics.gov.scot/data/{eid}"
    try:
        n=int(q(f'PREFIX qb: <http://purl.org/linked-data/cube#> SELECT (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{ds}> }}')[0]["n"])
    except Exception as e:
        n=-1
        print("ERR",eid,e)
    total+=max(0,n)
    print(f"{n:>10}  {eid}")
print("TOTAL", total)
