import subsets_utils as su
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
# carbonflux iso_summary full schema
for name in ["carbonflux_iso_summary","carbonflux_iso_change"]:
    v=resolve(name); fr=su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]
    metrics=[f['name'] for f in fr if f['data_type']=='numeric']
    print(f"\n=== {name} {v} numeric metric cols ===")
    for m in metrics: print("  ",m)
# verify carbonflux_iso_change agg
name="carbonflux_iso_change"; v=resolve(name)
sql=('SELECT iso, "umd_tree_cover_loss__year" AS year, SUM("umd_tree_cover_loss__ha") AS tcl_ha, '
     'SUM("gfw_full_extent_gross_emissions_biomass_soil__Mg_CO2e") AS emis, '
     'SUM("gfw_full_extent_gross_removals__Mg_CO2") AS removals '
     'FROM data GROUP BY iso, "umd_tree_cover_loss__year"')
r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=300)
print("\ncf iso_change agg status",r.status_code,"rows",len(r.text.strip().splitlines())-1)
print("  ","\n  ".join(r.text.strip().splitlines()[:3]))
# verify carbonflux_iso_summary agg with several metrics
name="carbonflux_iso_summary"; v=resolve(name)
sql=('SELECT iso, "umd_tree_cover_density_2000__threshold" AS threshold, '
     'SUM("gfw_flux_model_extent__ha") AS flux_extent_ha '
     'FROM data GROUP BY iso, "umd_tree_cover_density_2000__threshold"')
r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=300)
print("cf iso_summary agg status",r.status_code,"rows",len(r.text.strip().splitlines())-1)
