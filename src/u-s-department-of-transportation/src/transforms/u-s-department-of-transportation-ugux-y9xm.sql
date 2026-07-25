-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    CAST("objectid" AS BIGINT) AS objectid,
    "colldate",
    "railroad",
    CAST("milepost" AS BIGINT) AS milepost,
    "source",
    CAST("lat" AS DOUBLE) AS lat,
    "stfips",
    CAST("long" AS DOUBLE) AS long,
    "stcyfips",
    "stateab"
FROM "u-s-department-of-transportation-ugux-y9xm"
