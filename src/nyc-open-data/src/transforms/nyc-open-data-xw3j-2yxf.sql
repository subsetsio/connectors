-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "address",
    "bbl",
    "bin",
    "boro",
    "borocd",
    "city",
    "districtcode",
    "_name" AS name,
    "objectid",
    "state",
    "_type" AS type,
    "zip",
    "point"
FROM "nyc-open-data-xw3j-2yxf"
