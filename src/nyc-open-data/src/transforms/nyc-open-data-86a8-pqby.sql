-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inventory_id",
    "prop_id",
    "feature",
    "_type" AS type,
    "category",
    "subcategory"
FROM "nyc-open-data-86a8-pqby"
