-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    CAST("year" AS BIGINT) AS year,
    "month",
    CAST("vol_spec_fuel" AS BIGINT) AS vol_spec_fuel,
    "data_type",
    CAST("date_modified" AS TIMESTAMP) AS date_modified
FROM "u-s-department-of-transportation-5n49-mh85"
