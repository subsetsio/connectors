-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "source_id",
    "feat_code",
    "sub_code",
    "_name" AS name,
    "status",
    "shape_leng"
FROM "nyc-open-data-anc7-97cy"
