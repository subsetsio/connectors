-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "elderly_pop",
    "flat_type",
    "percentage"
FROM "sg-data-d-6c678a9e6cf49086c1fea012c40ceafe"
