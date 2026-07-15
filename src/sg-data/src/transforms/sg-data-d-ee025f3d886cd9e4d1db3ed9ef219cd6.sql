-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "citizenship",
    "semester",
    "fees",
    "reference"
FROM "sg-data-d-ee025f3d886cd9e4d1db3ed9ef219cd6"
