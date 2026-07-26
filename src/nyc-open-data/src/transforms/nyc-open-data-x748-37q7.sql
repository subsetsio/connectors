-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "source_id",
    "feature_co",
    "sub_featur",
    "bin",
    "status",
    "globalid"
FROM "nyc-open-data-x748-37q7"
