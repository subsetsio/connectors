-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "retirement_and_reemployment",
    "public_service_sector",
    "year",
    "staff_strength"
FROM "sg-data-d-9f7941e9ac89528b15473433a0d0a2f6"
