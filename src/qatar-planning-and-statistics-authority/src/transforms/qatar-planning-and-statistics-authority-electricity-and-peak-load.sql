-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "load_factor",
    "utilization_coefficient",
    "generation_gwh",
    "peak_load_mw",
    "installed_capacity_mw"
FROM "qatar-planning-and-statistics-authority-electricity-and-peak-load"
