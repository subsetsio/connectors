-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "section_" AS section,
    "shape_area",
    "the_geom",
    "shape_len"
FROM "nyc-open-data-jsdz-u4b8"
