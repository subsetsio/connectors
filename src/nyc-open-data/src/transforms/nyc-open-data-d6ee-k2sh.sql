-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sam",
    "sam_link",
    "subcategory",
    "total"
FROM "nyc-open-data-d6ee-k2sh"
