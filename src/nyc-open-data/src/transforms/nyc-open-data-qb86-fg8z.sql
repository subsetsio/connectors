-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_id",
    "_name" AS name,
    "tax_id"
FROM "nyc-open-data-qb86-fg8z"
