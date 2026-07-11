-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix poverty measures and administrative levels; filter admin_level and measure-specific columns before comparing rates.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin_level",
    "resource_hdx_id",
    "mpi",
    "headcount_ratio",
    "intensity_of_deprivation",
    "vulnerable_to_poverty",
    "in_severe_poverty",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-food-security-nutrition-poverty-poverty-rate"
