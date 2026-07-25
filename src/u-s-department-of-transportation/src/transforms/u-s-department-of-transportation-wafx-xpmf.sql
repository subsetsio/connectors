-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "state",
    "area",
    "system",
    "vehicle_type",
    CAST("percent_annual_distance" AS DOUBLE) AS percent_annual_distance
FROM "u-s-department-of-transportation-wafx-xpmf"
