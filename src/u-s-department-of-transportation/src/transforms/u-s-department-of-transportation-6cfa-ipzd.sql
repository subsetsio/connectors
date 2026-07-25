-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("sysid" AS BIGINT) AS sysid,
    CAST("year" AS DOUBLE) AS year,
    CAST("assigned_month" AS DOUBLE) AS assigned_month,
    CAST("docked" AS DOUBLE) AS docked,
    CAST("membership" AS DOUBLE) AS membership,
    CAST("wkend" AS DOUBLE) AS wkend,
    CAST("sum_min" AS DOUBLE) AS sum_min,
    CAST("num_trip" AS DOUBLE) AS num_trip,
    CAST("sum_level" AS DOUBLE) AS sum_level,
    CAST("hour" AS DOUBLE) AS hour,
    "sysname",
    "sysname_alt",
    CAST("pct_change" AS DOUBLE) AS pct_change,
    CAST("point_change" AS DOUBLE) AS point_change,
    CAST("sf_trip" AS DOUBLE) AS sf_trip,
    CAST("yr_mo_d" AS TIMESTAMP) AS yr_mo_d,
    CAST("avg_min" AS DOUBLE) AS avg_min,
    CAST("total_trips" AS DOUBLE) AS total_trips,
    CAST("total_trips_2019" AS DOUBLE) AS total_trips_2019,
    CAST("num_trips_2019" AS DOUBLE) AS num_trips_2019
FROM "u-s-department-of-transportation-6cfa-ipzd"
