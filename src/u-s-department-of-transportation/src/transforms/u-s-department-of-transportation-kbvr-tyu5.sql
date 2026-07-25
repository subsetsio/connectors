-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "state",
    CAST("value" AS BIGINT) AS value,
    CAST("date" AS TIMESTAMP) AS date,
    "fuel_type",
    CAST("fuel_type_code" AS BIGINT) AS fuel_type_code,
    CAST("fips" AS BIGINT) AS fips,
    "abbrev"
FROM "u-s-department-of-transportation-kbvr-tyu5"
