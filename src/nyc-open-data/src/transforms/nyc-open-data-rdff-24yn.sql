-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "_name" AS name,
    "boroname",
    "borocode",
    "subarea",
    "_source" AS source
FROM "nyc-open-data-rdff-24yn"
