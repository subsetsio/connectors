-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "flat_type",
    "no_of_households"
FROM "sg-data-d-db69c88a1ff684356b8b38dc0e9b432c"
