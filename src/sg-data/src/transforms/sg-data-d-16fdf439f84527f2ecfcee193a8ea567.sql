-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "gross_monthly_income_excl_emr_cpf",
    "occupation",
    "employed"
FROM "sg-data-d-16fdf439f84527f2ecfcee193a8ea567"
