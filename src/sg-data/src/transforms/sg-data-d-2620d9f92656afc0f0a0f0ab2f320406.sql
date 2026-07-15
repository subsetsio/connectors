-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "type",
    "age",
    "number"
FROM "sg-data-d-2620d9f92656afc0f0a0f0ab2f320406"
