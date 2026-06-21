import csv, io, json
from subsets_utils import get

# --- DTM: resolve current resource download URL via HDX CKAN ---
pkg = get(
    "https://data.humdata.org/api/3/action/package_show",
    params={"id": "global-iom-dtm-from-api"},
    timeout=(10.0, 120.0),
).json()["result"]
csv_res = [r for r in pkg["resources"] if (r.get("format") or "").lower() == "csv"]
print("=== DTM CKAN resources (csv) ===")
for r in csv_res:
    print(r["name"], "|", r.get("last_modified"), "|", r["url"])

dtm_url = csv_res[0]["url"]
r = get(dtm_url, timeout=(10.0, 180.0))
text = r.content.decode("utf-8-sig")
reader = csv.reader(io.StringIO(text))
header = next(reader)
rows = [next(reader) for _ in range(3)]
print("\n=== DTM header ===")
print(header)
print("\n=== DTM sample rows ===")
for row in rows:
    print(dict(zip(header, row)))

# --- Missing Migrants direct CSV ---
mm_url = "https://missingmigrants.iom.int/sites/g/files/tmzbdl601/files/report-migrant-incident/Missing_Migrants_Global_Figures_allData.csv"
r2 = get(mm_url, timeout=(10.0, 180.0))
text2 = r2.content.decode("utf-8-sig")
reader2 = csv.reader(io.StringIO(text2))
header2 = next(reader2)
rows2 = [next(reader2) for _ in range(3)]
print("\n=== MM header ===")
print(header2)
print("\n=== MM sample rows ===")
for row in rows2:
    print(dict(zip(header2, row)))
