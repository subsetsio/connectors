-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are alternative tree-canopy-density thresholds for the same country, not additive slices; choose one threshold before comparing or summing country totals.
SELECT
    "iso",
    "canopy_density_threshold",
    "flux_model_extent_ha",
    "area_ha",
    "tree_cover_extent_2000_ha",
    "gross_emissions_mg_co2e",
    "gross_removals_mg_co2",
    "net_flux_mg_co2e",
    "total_carbon_stock_2000_mg"
FROM "global-forest-watch-carbonflux-iso-summary"
