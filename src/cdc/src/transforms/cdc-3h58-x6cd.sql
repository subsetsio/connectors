-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "State" AS state,
    "County" AS county,
    "State FIPS Code" AS state_fips_code,
    "County FIPS Code" AS county_fips_code,
    CAST("Combined FIPS Code" AS BIGINT) AS combined_fips_code,
    CAST("Birth Rate" AS DOUBLE) AS birth_rate,
    CAST("Lower Confidence Limit" AS DOUBLE) AS lower_confidence_limit,
    CAST("Upper Confidence Limit" AS DOUBLE) AS upper_confidence_limit
FROM "cdc-3h58-x6cd"
