from subsets_utils import get
import csv, io

SPARQL = "https://statistics.gov.scot/sparql.csv"
def q(query):
    r = get(SPARQL, params={"query": query}, headers={"Accept":"text/csv"}, timeout=(10,120))
    r.raise_for_status()
    return list(csv.DictReader(io.StringIO(r.text)))

for slug in ["births", "Life-Expectancy", "deaths"]:
    ds = f"http://statistics.gov.scot/data/{slug}"
    print(f"\n===== {slug} components =====")
    rows = q(f'''
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?dim ?measure ?attr WHERE {{
      <{ds}> qb:structure ?dsd . ?dsd qb:component ?c .
      OPTIONAL {{ ?c qb:dimension ?dim }}
      OPTIONAL {{ ?c qb:measure ?measure }}
      OPTIONAL {{ ?c qb:attribute ?attr }}
    }}''')
    for r in rows:
        print("  dim=",r["dim"]," meas=",r["measure"]," attr=",r["attr"])
    # count observations
    cnt = q(f'PREFIX qb: <http://purl.org/linked-data/cube#> SELECT (COUNT(*) AS ?n) WHERE {{ ?o qb:dataSet <{ds}> }}')
    print("  observations:", cnt[0]["n"])
