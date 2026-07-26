-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "municourt",
    "borocode",
    "boroname",
    "the_geom",
    "shape_length",
    "shape_area"
FROM "nyc-open-data-mi5z-t7dx"
