import subsets_utils as su, json
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])

# Does server-side GROUP BY work keyless on /download/csv?
name="gadm__tcl__iso_change"; v=resolve(name)
sql=("SELECT iso, umd_tree_cover_loss__year AS year, umd_tree_cover_density_2000__threshold AS threshold, "
     "SUM(umd_tree_cover_loss__ha) AS tree_cover_loss_ha, "
     "SUM(gfw_full_extent_gross_emissions__Mg_CO2e) AS gross_emissions_co2e_mg "
     "FROM data GROUP BY iso, year, threshold ORDER BY iso, year, threshold")
r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=300)
print("tcl iso_change GROUP BY status", r.status_code)
lines=r.text.strip().splitlines()
print("rows returned:", len(lines)-1)
print("\n".join(lines[:6]))

# count distinct group size to be sure it's well under 90k
r2=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":"SELECT count(DISTINCT (iso, umd_tree_cover_loss__year, umd_tree_cover_density_2000__threshold)) AS g FROM data"},timeout=300)
print("distinct iso/year/threshold groups:", r2.text.strip().splitlines()[-1])
