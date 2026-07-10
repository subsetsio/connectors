-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("FIPS" AS BIGINT) AS fips,
    CAST("Year" AS BIGINT) AS year,
    "State" AS state,
    CAST("FIPS State" AS BIGINT) AS fips_state,
    "County" AS county,
    CAST("Population" AS BIGINT) AS population,
    CAST("Model-based Death Rate" AS DOUBLE) AS model_based_death_rate,
    CAST("Standard Deviation" AS DOUBLE) AS standard_deviation,
    CAST("Lower Confidence Limit" AS DOUBLE) AS lower_confidence_limit,
    CAST("Upper Confidence Limit" AS DOUBLE) AS upper_confidence_limit,
    "Urban/Rural Category" AS urban_rural_category,
    CAST("Census Division" AS BIGINT) AS census_division
FROM "cdc-rpvx-m2md"
