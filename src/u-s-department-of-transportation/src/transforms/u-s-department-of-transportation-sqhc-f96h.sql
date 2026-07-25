-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    CAST("objectid" AS BIGINT) AS objectid,
    "uniqueid",
    "city",
    "county",
    "state",
    "fips",
    "crossing_type",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "rrowner",
    "subdivision",
    "rail_milepost",
    "name",
    "bridge_type",
    "design_type",
    "num_tracks",
    CAST("length" AS BIGINT) AS length,
    "alt_name",
    "gradecrossing_id",
    "secondary_name",
    "secondary_rrowner",
    "secondary_streetnames",
    "secondary_subdivision",
    "secondary_railmilepost",
    "secondary_numtracks",
    "mile_post",
    CAST("createdate" AS TIMESTAMP) AS createdate,
    "source"
FROM "u-s-department-of-transportation-sqhc-f96h"
