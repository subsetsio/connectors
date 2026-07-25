-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("sysid" AS BIGINT) AS sysid,
    "sysname",
    CAST("year" AS BIGINT) AS year,
    CAST("assigned_month" AS BIGINT) AS assigned_month,
    CAST("hour" AS BIGINT) AS hour,
    CAST("trip_type" AS BIGINT) AS trip_type,
    CAST("sum_min" AS DOUBLE) AS sum_min,
    CAST("num_trip" AS BIGINT) AS num_trip,
    "sysname_alt"
FROM "u-s-department-of-transportation-j6uy-twhg"
