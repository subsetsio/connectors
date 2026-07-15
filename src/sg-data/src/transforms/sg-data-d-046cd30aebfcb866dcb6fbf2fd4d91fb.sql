-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "facility",
    "number"
FROM "sg-data-d-046cd30aebfcb866dcb6fbf2fd4d91fb"
