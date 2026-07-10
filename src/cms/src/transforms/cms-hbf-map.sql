-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "addr",
    "city",
    "state",
    "zip",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("lon" AS DOUBLE) AS lon
FROM "cms-hbf-map"
