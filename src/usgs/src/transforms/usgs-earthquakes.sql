-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "depth",
    "mag",
    "magType" AS magtype,
    "nst",
    "gap",
    "dmin",
    "rms",
    "net",
    "id",
    "updated",
    "place",
    "type",
    "horizontalError" AS horizontalerror,
    "depthError" AS deptherror,
    "magError" AS magerror,
    "magNst" AS magnst,
    "status",
    "locationSource" AS locationsource,
    "magSource" AS magsource
FROM "usgs-earthquakes"
