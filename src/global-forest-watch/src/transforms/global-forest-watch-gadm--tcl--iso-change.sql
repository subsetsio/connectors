-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are alternative tree-canopy-density thresholds for the same country and year, not additive slices; choose one threshold before comparing or summing loss totals.
SELECT
    "iso",
    "loss_year",
    "canopy_density_threshold",
    "tree_cover_loss_ha",
    "tree_cover_loss_from_fires_ha",
    "aboveground_biomass_loss_mg",
    "aboveground_co2_emissions_mg",
    "gross_emissions_mg_co2e"
FROM "global-forest-watch-gadm--tcl--iso-change"
