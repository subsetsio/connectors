-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "address",
    "boro",
    "borocd",
    "city",
    "fid",
    "globalid",
    "_name" AS name,
    "state",
    "_type" AS type,
    "zip",
    "point"
FROM "nyc-open-data-242c-ru4i"
