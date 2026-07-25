-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    CAST("date" AS TIMESTAMP) AS date,
    "mode",
    "trade",
    CAST("value" AS BIGINT) AS value
FROM "u-s-department-of-transportation-rjzd-p9xx"
