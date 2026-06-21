import csv, io
import duckdb
import pyarrow as pa
from nodes.gapminder import REPOS, _datapoint_resources, _get_json, _get_text, VALUES_SCHEMA, CONCEPT_KEYS

# Build a small values sample from first 3 datapoints of systema_globalis
base = REPOS["systema_globalis"]
dp = _get_json(base + "/datapackage.json")
res = list(_datapoint_resources(dp))
print("systema datapoint resources:", len(res))
batches = []
for path, geo_dim, indicator in res[:3]:
    text = _get_text(f"{base}/{path}")
    geos, times, vals = [], [], []
    for row in csv.DictReader(io.StringIO(text)):
        v = row.get(indicator)
        if not v:
            continue
        geos.append(row.get(geo_dim)); times.append(row.get("time")); vals.append(v)
    n = len(geos)
    batches.append(pa.table({
        "repo": pa.array(["systema_globalis"]*n, pa.string()),
        "geo_dim": pa.array([geo_dim]*n, pa.string()),
        "geo": pa.array(geos, pa.string()),
        "time": pa.array(times, pa.string()),
        "indicator": pa.array([indicator]*n, pa.string()),
        "value": pa.array(vals, pa.string()),
    }, schema=VALUES_SCHEMA))
vals_tbl = pa.concat_tables(batches)
print("values rows:", len(vals_tbl), "indicators:", set(vals_tbl.column("indicator").to_pylist()))

con = duckdb.connect()
con.register("gapminder-values", vals_tbl)
out = con.execute('''
    SELECT indicator, geo, geo_dim, TRY_CAST(time AS INTEGER) AS year,
           TRY_CAST(value AS DOUBLE) AS value, repo
    FROM "gapminder-values"
    WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL AND TRY_CAST(time AS INTEGER) IS NOT NULL
''').arrow().read_all()
print("values transform rows:", len(out))
print(out.slice(0, 3).to_pylist())

# concepts
rows = []
for repo, b in REPOS.items():
    text = _get_text(b + "/ddf--concepts.csv")
    for row in csv.DictReader(io.StringIO(text)):
        o = {k: (row.get(k) or None) for k in CONCEPT_KEYS}; o["repo"] = repo; rows.append(o)
print("concepts rows:", len(rows))
ctbl = pa.Table.from_pylist(rows)
con.register("gapminder-concepts", ctbl)
cout = con.execute('''
    SELECT concept, concept_type, name, name_short, description, unit, tags,
           scales, domain, source_url, repo
    FROM "gapminder-concepts" WHERE concept IS NOT NULL
''').arrow().read_all()
print("concepts transform rows:", len(cout))
print(cout.slice(0, 2).to_pylist())
