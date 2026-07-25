-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "month",
    CAST("year" AS BIGINT) AS year,
    "tax_type",
    CAST("value" AS DOUBLE) AS value,
    CAST("fips_state" AS BIGINT) AS fips_state,
    CAST("numeric_month" AS BIGINT) AS numeric_month,
    "note",
    "id"
FROM "u-s-department-of-transportation-3qgg-2u2a"
