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
FROM "sg-data-d-bab55a1cdaba1b86a46323cf567d6be5"
