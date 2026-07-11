-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix administrative levels, gender, and age ranges; filter admin_level, gender, min_age, and max_age before summing population.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "gender",
    "age_range",
    "min_age",
    "max_age",
    "population",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-geography-infrastructure-baseline-population"
