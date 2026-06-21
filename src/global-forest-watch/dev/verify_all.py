import subsets_utils as su
BASE="https://data-api.globalforestwatch.org"
def resolve(name): return max(su.get(f"{BASE}/dataset/{name}",timeout=60).json()["data"]["versions"])
Q={
"fao_forest_extent":'SELECT iso, country, desk_study, year, "primary (ha)" AS primary_ha, "naturally regenerating forest (ha)" AS naturally_regenerating_forest_ha, "planted forest (ha)" AS planted_forest_ha, "forest (ha)" AS forest_ha, "non-forest (ha)" AS non_forest_ha, "total land area (ha)" AS total_land_area_ha FROM data',
"fao_forest_change":'SELECT iso, country, desk_study, year, "reforestation (ha per year)" AS reforestation_ha_per_year, "forest expansion (ha per year)" AS forest_expansion_ha_per_year, "deforestation (ha per year)" AS deforestation_ha_per_year FROM data',
"fao_forestry_employment":'SELECT iso, country, desk_study, year, "silviculture and other (FTE)" AS silviculture_and_other_fte, "logging (FTE)" AS logging_fte, "gathering (FTE)" AS gathering_fte, "support (FTE)" AS support_fte, "all (FTE)" AS all_fte, "female (FTE)" AS female_fte FROM data',
"gadm__tcl__iso_change":'SELECT iso, "umd_tree_cover_loss__year" AS year, "umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, SUM("umd_tree_cover_loss__ha") AS tree_cover_loss_ha, SUM("umd_tree_cover_loss_from_fires__ha") AS tree_cover_loss_from_fires_ha, SUM("whrc_aboveground_biomass_loss__Mg") AS aboveground_biomass_loss_mg, SUM("whrc_aboveground_co2_emissions__Mg") AS aboveground_co2_emissions_mg, SUM("gfw_full_extent_gross_emissions__Mg_CO2e") AS gross_emissions_co2e_mg FROM data GROUP BY iso, "umd_tree_cover_loss__year", "umd_tree_cover_density_2000__threshold"',
"gadm__tcl__iso_summary":'SELECT iso, "umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, SUM("umd_tree_cover_extent_2000__ha") AS tree_cover_extent_2000_ha, SUM("umd_tree_cover_extent_2010__ha") AS tree_cover_extent_2010_ha, SUM("umd_tree_cover_gain__ha") AS tree_cover_gain_ha, SUM("umd_tree_cover_loss__ha") AS tree_cover_loss_ha, SUM("area__ha") AS area_ha, SUM("gfw_aboveground_carbon_stocks_2000__Mg_C") AS aboveground_carbon_stocks_2000_mg_c, SUM("whrc_aboveground_biomass_stock_2000__Mg") AS aboveground_biomass_stock_2000_mg FROM data GROUP BY iso, "umd_tree_cover_density_2000__threshold"',
"carbonflux_iso_summary":'SELECT iso, "umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, SUM("gfw_flux_model_extent__ha") AS flux_model_extent_ha, SUM("gfw_full_extent_gross_emissions_biomass_soil__Mg_CO2e") AS gross_emissions_co2e_mg, SUM("gfw_full_extent_gross_removals__Mg_CO2") AS gross_removals_co2_mg FROM data GROUP BY iso, "umd_tree_cover_density_2000__threshold"',
"gadm__integrated_alerts__iso_daily_alerts":'SELECT iso, CAST(date_part(\'year\',"gfw_integrated_alerts__date") AS INTEGER) AS year, CAST(date_part(\'month\',"gfw_integrated_alerts__date") AS INTEGER) AS month, "gfw_integrated_alerts__confidence" AS confidence, SUM("alert__count") AS alert_count, SUM("alert_area__ha") AS alert_area_ha FROM data WHERE "gfw_integrated_alerts__date" IS NOT NULL GROUP BY iso, year, month, confidence',
"wri_global_power_plant_database":'SELECT * FROM data',
"gfw_universal_mill_list":'SELECT gfw_fid, uml_id, parent_com, mill_name, rspo_statu, rspo_type, date_rspo_, latitude, longitude, country, province, district, confidence, alternativ, "gfw_area__ha" AS gfw_area_ha, gfw_geostore_id, created_on, updated_on FROM data',
}
for name,sql in Q.items():
    try:
        v=resolve(name)
        r=su.get(f"{BASE}/dataset/{name}/{v}/download/csv",params={"sql":sql},timeout=300)
        lines=r.text.strip().splitlines()
        head=lines[0] if r.status_code==200 else r.text[:120]
        print(f"[{r.status_code}] {name} {v} rows={len(lines)-1 if r.status_code==200 else '-'}")
        if r.status_code==200: print("       header:", head[:160])
        else: print("       ERR:", head)
    except Exception as e:
        print(f"[EXC] {name}: {type(e).__name__} {e}")
