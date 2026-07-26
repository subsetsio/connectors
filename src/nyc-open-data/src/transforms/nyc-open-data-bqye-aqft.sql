-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "_name" AS name,
    "_year" AS year,
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-bqye-aqft"
