-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    "indicator",
    CAST("week_number" AS BIGINT) AS week_number,
    CAST("week_ending" AS TIMESTAMP) AS week_ending,
    CAST("week_current" AS DOUBLE) AS week_current,
    CAST("week_baseline" AS DOUBLE) AS week_baseline,
    CAST("week_lowest_date" AS TIMESTAMP) AS week_lowest_date,
    CAST("week_lowest" AS DOUBLE) AS week_lowest
FROM "u-s-department-of-transportation-75qq-qmj6"
