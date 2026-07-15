-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "percentage_psle_science"
FROM "sg-data-d-078f6d42ad39d1a80c505d0b3fc7c90f"
