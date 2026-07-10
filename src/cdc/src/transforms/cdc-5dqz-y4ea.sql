-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "as_of",
    "disease",
    "state",
    "date",
    CAST("median" AS DOUBLE) AS median,
    CAST("lower" AS DOUBLE) AS lower,
    CAST("upper" AS DOUBLE) AS upper,
    CAST("interval_width" AS DOUBLE) AS interval_width,
    CAST("p_growing" AS DOUBLE) AS p_growing,
    "category",
    "BuildNumber" AS buildnumber
FROM "cdc-5dqz-y4ea"
