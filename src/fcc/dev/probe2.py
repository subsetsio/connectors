from subsets_utils import get
rid = "2ra3-4jd4"  # small (7423 rows) to inspect headers/format
# SODA resource CSV with field-name headers
r = get(f"https://opendata.fcc.gov/resource/{rid}.csv", params={"$limit": 3, "$order": ":id"}, timeout=(10,120))
print("RESOURCE.CSV status", r.status_code)
print(r.text[:400])
print("=====")
# Big $limit on resource csv — does it return all rows?
r2 = get(f"https://opendata.fcc.gov/resource/{rid}.csv", params={"$limit": 100000000}, timeout=(10,300))
print("RESOURCE.CSV biglimit lines:", r2.text.count("\n"))
print("=====")
# Export endpoint
r3 = get(f"https://opendata.fcc.gov/api/views/{rid}/rows.csv", params={"accessType":"DOWNLOAD"}, timeout=(10,300))
print("EXPORT rows.csv status", r3.status_code, "lines:", r3.text.count("\n"))
print(r3.text[:300])
