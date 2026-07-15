-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "flat_type",
    "average_size",
    "median_size"
FROM "sg-data-d-3b626812cc3ea5cafa20490bb996eb0b"
