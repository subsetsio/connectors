-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "elderly_pop",
    "sex",
    "age",
    "percentage"
FROM "sg-data-d-c24f6b8078ee721f7191906ca1b3a367"
