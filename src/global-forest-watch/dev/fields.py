import subsets_utils as su, json
BASE="https://data-api.globalforestwatch.org"
def resolve(name):
    return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
for name in ["gadm__tcl__iso_summary","gadm__integrated_alerts__iso_daily_alerts","gadm__viirs__adm2_daily_alerts","carbonflux_iso_summary","fao_forestry_employment","nasa_viirs_fire_alerts","umd_adm0_net_tree_cover_change_from_height"]:
    v=resolve(name)
    r=su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60)
    fs=r.json()["data"]
    print("\n===",name,v,"===")
    for f in fs:
        print(f"  {f.get('name')}: {f.get('data_type')}")
