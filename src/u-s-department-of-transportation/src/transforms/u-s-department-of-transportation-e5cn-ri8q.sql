-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "state",
    CAST("rate" AS DOUBLE) AS rate,
    "fuel_type",
    "fuel_type_code",
    CAST("fips" AS BIGINT) AS fips,
    "abbrev",
    "note",
    CAST("effective_date" AS TIMESTAMP) AS effective_date,
    CAST("year" AS BIGINT) AS year
FROM "u-s-department-of-transportation-e5cn-ri8q"
