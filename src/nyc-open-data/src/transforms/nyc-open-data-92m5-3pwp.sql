-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "descriptio",
    "feat_code",
    "source_id",
    "sub_code",
    "status",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-92m5-3pwp"
