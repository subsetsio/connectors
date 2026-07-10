-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week Ending" AS week_ending,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    "Enrollment Date" AS enrollment_date,
    "As of date" AS as_of_date,
    "Race and ethnicity" AS race_and_ethnicity
FROM "cdc-nqu5-vn7d"
