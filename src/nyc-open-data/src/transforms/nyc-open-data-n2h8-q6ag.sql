-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "shape_area",
    "shape_leng",
    "borocd",
    "cd",
    "borocd_1",
    "shape_le_1",
    "shape_ar_1",
    "franchisee",
    "color",
    "borough"
FROM "nyc-open-data-n2h8-q6ag"
