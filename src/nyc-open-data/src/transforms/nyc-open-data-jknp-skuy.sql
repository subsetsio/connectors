-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "on_street",
    "from_stree",
    "to_street",
    "humps",
    "date_insta",
    "shape_stle"
FROM "nyc-open-data-jknp-skuy"
