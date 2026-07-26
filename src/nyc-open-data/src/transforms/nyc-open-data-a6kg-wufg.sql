-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "taxomony_id",
    "_name" AS name,
    "parent_id",
    "parent_name"
FROM "nyc-open-data-a6kg-wufg"
