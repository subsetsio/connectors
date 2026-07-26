-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "cb2000",
    "bctcb2000",
    "borocode",
    "boroname",
    "ct2000",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-t3ph-3ztd"
