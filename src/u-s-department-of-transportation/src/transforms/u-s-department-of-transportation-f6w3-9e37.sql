-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("year" AS BIGINT) AS year,
    "ru",
    "f_system",
    "state",
    CAST("mileage" AS DOUBLE) AS mileage,
    CAST("lane_miles" AS DOUBLE) AS lane_miles,
    CAST("vmt" AS BIGINT) AS vmt,
    CAST("fatalities" AS BIGINT) AS fatalities
FROM "u-s-department-of-transportation-f6w3-9e37"
