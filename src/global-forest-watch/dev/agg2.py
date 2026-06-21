import subsets_utils as su
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
name="gadm__tcl__iso_change"; v=resolve(name)
sql=('SELECT iso, "umd_tree_cover_loss__year" AS year, "umd_tree_cover_density_2000__threshold" AS threshold, '
     'SUM("umd_tree_cover_loss__ha") AS tree_cover_loss_ha, '
     'SUM("gfw_full_extent_gross_emissions__Mg_CO2e") AS gross_emissions_co2e_mg '
     'FROM data GROUP BY iso, "umd_tree_cover_loss__year", "umd_tree_cover_density_2000__threshold" '
     'ORDER BY iso, year, threshold')
r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=300)
print("status", r.status_code)
lines=r.text.strip().splitlines()
print("rows:", len(lines)-1)
print("\n".join(lines[:8]))
