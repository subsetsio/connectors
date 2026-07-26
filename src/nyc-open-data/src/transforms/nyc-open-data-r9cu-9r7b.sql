-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "source_id",
    "sub_code",
    "feat_code",
    "_name" AS name,
    "status",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-r9cu-9r7b"
