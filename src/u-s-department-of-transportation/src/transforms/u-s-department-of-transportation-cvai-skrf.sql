-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "the_geom",
    CAST("sysid" AS DOUBLE) AS sysid,
    CAST("sum_min" AS DOUBLE) AS sum_min,
    CAST("num_trip" AS DOUBLE) AS num_trip,
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lng" AS DOUBLE) AS lng,
    "sysname",
    CAST("year" AS DOUBLE) AS year,
    CAST("assigned_month" AS DOUBLE) AS assigned_month,
    CAST("pct_ttl_num_trips" AS DOUBLE) AS pct_ttl_num_trips,
    CAST("bin_num_trip" AS DOUBLE) AS bin_num_trip,
    CAST("mar_ind" AS DOUBLE) AS mar_ind,
    CAST("sysorder" AS DOUBLE) AS sysorder,
    CAST("may_ind" AS DOUBLE) AS may_ind,
    "datestr",
    "datetxt",
    CAST("display" AS DOUBLE) AS display,
    "sysname_alt",
    CAST("yroverchange" AS DOUBLE) AS yroverchange,
    CAST("yroverchange_bin" AS BIGINT) AS yroverchange_bin,
    CAST("trip_type" AS DOUBLE) AS trip_type
FROM "u-s-department-of-transportation-cvai-skrf"
