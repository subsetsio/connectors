-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "title",
    "description"
FROM "sg-data-d-4d2c99ea159f1f6dd67beb58bf9cbe8d"
