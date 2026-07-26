-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_type" AS type,
    "locationid",
    "the_geom",
    "_name" AS name,
    "latitude",
    "longitude"
FROM "nyc-open-data-3we2-bw9s"
