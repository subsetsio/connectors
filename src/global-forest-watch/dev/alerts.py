import subsets_utils as su
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
def run(name,sql,t=300):
    v=resolve(name); r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=t)
    return v,r.status_code,r.text

# integrated iso daily -> monthly agg
name="gadm__integrated_alerts__iso_daily_alerts"
sql=('SELECT iso, date_part(\'year\',"gfw_integrated_alerts__date") AS year, date_part(\'month\',"gfw_integrated_alerts__date") AS month, '
     '"gfw_integrated_alerts__confidence" AS confidence, SUM("alert__count") AS alert_count, SUM("alert_area__ha") AS alert_area_ha '
     'FROM data GROUP BY iso,year,month,confidence')
v,sc,t=run(name,sql); print("integrated iso monthly:",v,sc,"rows",len(t.strip().splitlines())-1); print(" ", "\n  ".join(t.strip().splitlines()[:3]))

# glad iso weekly fields check
for name in ["gadm__glad__iso_weekly_alerts","gadm__viirs__iso_weekly_alerts"]:
    v=resolve(name); fr=[f['name'] for f in su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]]
    print(name, "has year/week cols:", [c for c in fr if 'year' in c or 'week' in c or 'confidence' in c.lower() or 'count' in c])

# viirs iso weekly agg (iso, year, week, confidence)
name="gadm__viirs__iso_weekly_alerts"
sql=('SELECT iso, "alert__year" AS year, "alert__week" AS week, "confidence__cat" AS confidence, SUM("alert__count") AS alert_count '
     'FROM data GROUP BY iso,"alert__year","alert__week","confidence__cat"')
v,sc,t=run(name,sql); print("viirs iso weekly agg:",v,sc,"rows",len(t.strip().splitlines())-1)

# glad iso weekly agg
name="gadm__glad__iso_weekly_alerts"
v=resolve(name); fr=[f['name'] for f in su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]]
print("glad iso_weekly all cols:", fr)
