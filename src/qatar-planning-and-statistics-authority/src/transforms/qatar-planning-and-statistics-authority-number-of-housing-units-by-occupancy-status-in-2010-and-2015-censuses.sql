-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occupancy_status",
    "kyfy_lshgl",
    "census_2015_t_dd_2015",
    "census_2010_t_dd_2010",
    "increase_decrease",
    "percentage_of_increase_decrease"
FROM "qatar-planning-and-statistics-authority-number-of-housing-units-by-occupancy-status-in-2010-and-2015-censuses"
