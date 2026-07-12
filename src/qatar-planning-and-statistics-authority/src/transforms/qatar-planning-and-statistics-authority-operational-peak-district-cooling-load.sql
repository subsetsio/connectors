-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "dc_plant_peak_cooling_load_tr",
    "dc_plant_installed_cooling_capacity_tr"
FROM "qatar-planning-and-statistics-authority-operational-peak-district-cooling-load"
