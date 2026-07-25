-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    "vehicle_type",
    "time_period",
    "area",
    CAST("f_system" AS BIGINT) AS f_system,
    CAST("median_speed" AS DOUBLE) AS median_speed,
    CAST("median_speed_previousmonth" AS DOUBLE) AS median_speed_previousmonth,
    CAST("median_speed_previousyear" AS DOUBLE) AS median_speed_previousyear,
    CAST("median_speed_2019" AS DOUBLE) AS median_speed_2019
FROM "u-s-department-of-transportation-ra4w-8xud"
