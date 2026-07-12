-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "annual_cooling_energy_production_million_tr",
    "plant_utilization",
    "peak_cooling_load_tr",
    "connected_load_tr",
    "installed_cooling_capacity_tr",
    "lnsht_lqtsdy"
FROM "qatar-planning-and-statistics-authority-district-cooling-plant-characteristics-by-economic-activity"
