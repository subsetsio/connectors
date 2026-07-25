-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    CAST("sysid" AS DOUBLE) AS sysid,
    CAST("year" AS DOUBLE) AS year,
    CAST("month" AS DOUBLE) AS month,
    CAST("groupid" AS DOUBLE) AS groupid,
    "e_station_" AS e_station,
    CAST("sum_min" AS DOUBLE) AS sum_min,
    CAST("num_trip" AS DOUBLE) AS num_trip,
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lon" AS DOUBLE) AS lon,
    "e_station_name",
    CAST("pct_ttl_num_trip" AS DOUBLE) AS pct_ttl_num_trip,
    CAST("bin_num_trips" AS DOUBLE) AS bin_num_trips,
    "sysname"
FROM "u-s-department-of-transportation-w3m5-t2w3"
