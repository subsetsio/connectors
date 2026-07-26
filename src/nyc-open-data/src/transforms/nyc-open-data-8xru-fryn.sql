-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "loccode",
    "prek_type",
    "borough",
    "district",
    "_name" AS name,
    "phone",
    "address",
    "zip",
    "day_length",
    "area_name",
    "seats"
FROM "nyc-open-data-8xru-fryn"
