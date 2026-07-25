-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    "indicator",
    CAST("week_num" AS DOUBLE) AS week_num,
    CAST("date" AS TIMESTAMP) AS date,
    CAST("current" AS BIGINT) AS current,
    CAST("baseline" AS BIGINT) AS baseline,
    "lowest_date",
    "lowest"
FROM "u-s-department-of-transportation-btpt-uxhx"
