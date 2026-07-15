-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cc_rating",
    "number"
FROM "sg-data-d-3e182eb6d9d7eb78addb26a9c7179204"
