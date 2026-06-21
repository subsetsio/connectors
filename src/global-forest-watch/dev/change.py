import subsets_utils as su, json
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
for name in ["gadm__tcl__iso_change","gadm__tcl__adm1_change","carbonflux_iso_change","umd_adm0_net_tree_cover_change_from_height","fao_forestry_employment","fao_forest_extent","fao_forest_change"]:
    v=resolve(name)
    fr=su.get(f"{BASE}/dataset/{name}/{v}/fields",timeout=60).json()["data"]
    cr=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":"SELECT count(*) AS n FROM data"},timeout=180)
    n=cr.text.strip().splitlines()[-1] if cr.status_code==200 else cr.status_code
    print(f"\n=== {name} {v}  rows={n} ncols={len(fr)} ===")
    print("  cols:", [f["name"] for f in fr])
