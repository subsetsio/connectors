-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "gross_monthly_income_excl_emr_cpf",
    "age",
    "employed"
FROM "sg-data-d-c0e11e1f0e2cfc380209d2924dfb28c2"
