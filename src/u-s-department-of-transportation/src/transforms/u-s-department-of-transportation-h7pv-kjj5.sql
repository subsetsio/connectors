-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    "indicator",
    CAST("week_number" AS BIGINT) AS week_number,
    CAST("week_ending" AS TIMESTAMP) AS week_ending,
    CAST("week_change" AS DOUBLE) AS week_change
FROM "u-s-department-of-transportation-h7pv-kjj5"
