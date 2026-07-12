-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_operational_dc_plants",
    "operational_dc_plants_using_non_potable_water",
    "operational_dc_plants_using_potable_water"
FROM "qatar-planning-and-statistics-authority-operational-district-cooling-plants"
