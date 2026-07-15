-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "percentage_psle_mtl"
FROM "sg-data-d-4e0be8a8b4cb7fc3b43f2c82d9799fc2"
