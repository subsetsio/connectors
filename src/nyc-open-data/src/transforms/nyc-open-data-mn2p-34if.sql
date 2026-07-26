-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "make",
    "model",
    "hybridnonhybrid",
    "standard_type",
    "epa_rating_city",
    "vehicle_count",
    "total_actual_miles",
    "total_actual_fuel",
    "epa_expected_fuel",
    "actual_fuel_economy_geotab",
    "percent_difference_actual_to_epa",
    "estimated_fuel_costs_per_gallon",
    "fuel_costs_per_mile"
FROM "nyc-open-data-mn2p-34if"
