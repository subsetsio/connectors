-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "the_geom",
    CAST("strt_sysid" AS DOUBLE) AS strt_sysid,
    CAST("end_sysid" AS BIGINT) AS end_sysid,
    "strt_facid",
    "end_facid",
    CAST("trip_time" AS BIGINT) AS trip_time,
    CAST("accessible_stations" AS BIGINT) AS accessible_stations,
    CAST("total_stations" AS BIGINT) AS total_stations,
    CAST("nyc_borough" AS BIGINT) AS nyc_borough,
    "nyc_borough_name",
    CAST("sf_area" AS BIGINT) AS sf_area
FROM "u-s-department-of-transportation-xjbt-2jz9"
