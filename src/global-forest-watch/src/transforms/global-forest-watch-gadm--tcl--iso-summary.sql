-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are alternative tree-canopy-density thresholds for the same country, not additive slices; choose one threshold before comparing or summing country totals.
SELECT
    "iso",
    "canopy_density_threshold",
    "area_ha",
    "tree_cover_extent_2000_ha",
    "tree_cover_extent_2010_ha",
    "tree_cover_gain_ha",
    "tree_cover_loss_ha",
    "tree_cover_loss_from_fires_ha",
    "aboveground_carbon_stocks_2000_mg_c",
    "belowground_carbon_stocks_2000_mg_c",
    "soil_carbon_stocks_2000_mg_c",
    "aboveground_biomass_stock_2000_mg",
    "gross_emissions_mg_co2e",
    "gross_removals_mg_co2",
    "net_flux_mg_co2e"
FROM "global-forest-watch-gadm--tcl--iso-summary"
