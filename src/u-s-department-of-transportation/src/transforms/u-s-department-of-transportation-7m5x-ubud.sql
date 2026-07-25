-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "the_geom",
    CAST("id" AS BIGINT) AS id,
    "fac_id",
    "bike_id",
    CAST("system_id" AS BIGINT) AS system_id,
    "system_name",
    CAST("year" AS BIGINT) AS year,
    CAST("asofdate" AS BIGINT) AS asofdate,
    "fac_name",
    "address",
    "city",
    "state",
    "zipcode",
    "cbsa_code",
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("latitude" AS DOUBLE) AS latitude,
    "station_type",
    "launchdate",
    "enddate"
FROM "u-s-department-of-transportation-7m5x-ubud"
