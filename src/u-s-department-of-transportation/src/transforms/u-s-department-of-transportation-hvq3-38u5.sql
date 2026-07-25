-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    "indicator",
    CAST("date" AS TIMESTAMP) AS date,
    CAST("current" AS BIGINT) AS current,
    CAST("week_number" AS BIGINT) AS week_number,
    CAST("year" AS BIGINT) AS year
FROM "u-s-department-of-transportation-hvq3-38u5"
