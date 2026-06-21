import subsets_utils as su
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
def run(name,sql,timeout=300):
    v=resolve(name)
    r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=timeout)
    return v,r.status_code,r.text

# power plant + mill list: plain selects, get count + cols
for name in ["wri_global_power_plant_database","gfw_universal_mill_list"]:
    v,sc,t=run(name,"SELECT count(*) AS n FROM data")
    fr=su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]
    print(f"{name} {v} rows={t.strip().splitlines()[-1] if sc==200 else sc} ncols={len(fr)}")
    print("  cols:", [f['name'] for f in fr][:30])

# tcl iso_summary aggregated (no year)
name="gadm__tcl__iso_summary"
sql=('SELECT iso, "umd_tree_cover_density_2000__threshold" AS threshold, '
     'SUM("umd_tree_cover_extent_2000__ha") AS tc_extent_2000_ha, '
     'SUM("umd_tree_cover_loss__ha") AS tc_loss_ha, '
     'SUM("umd_tree_cover_gain__ha") AS tc_gain_ha '
     'FROM data GROUP BY iso, "umd_tree_cover_density_2000__threshold"')
v,sc,t=run(name,sql); print("tcl iso_summary agg", v, sc, "rows", len(t.strip().splitlines())-1)

# carbonflux iso_summary agg
name="carbonflux_iso_summary"
sql='SELECT iso, "umd_tree_cover_density_2000__threshold" AS threshold, SUM("gfw_flux_model_extent__ha") AS flux_extent_ha FROM data GROUP BY iso,"umd_tree_cover_density_2000__threshold"'
v,sc,t=run(name,sql); print("carbonflux iso_summary agg", v, sc, "rows", len(t.strip().splitlines())-1)

# glad iso summary agg - first see fields
for name in ["gadm__glad__iso_summary","gadm__viirs__iso_weekly_alerts"]:
    v=resolve(name); fr=su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]
    print(f"\n{name} {v} cols:", [f['name'] for f in fr])
