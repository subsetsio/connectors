-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "source_id",
    "feature_code",
    "sub_code",
    "_name" AS name,
    "status",
    "shape_area",
    "shape_len"
FROM "nyc-open-data-b7j8-z8a7"
