-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "State" AS state,
    "FIPS" AS fips,
    "Case_status" AS case_status,
    "Sex" AS sex,
    "Age_cat_yrs" AS age_cat_yrs,
    CAST("Frequency" AS BIGINT) AS frequency
FROM "cdc-x5j9-wybp"
