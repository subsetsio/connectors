-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "month",
    "commodity",
    CAST("monthly_tons" AS BIGINT) AS monthly_tons,
    CAST("percent" AS DOUBLE) AS percent
FROM "u-s-department-of-transportation-b5ay-n4yn"
