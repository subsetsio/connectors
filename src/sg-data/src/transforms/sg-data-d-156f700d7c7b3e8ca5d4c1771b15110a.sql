-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "gross_monthly_income_excl_emr_cpf",
    "highest_qualification",
    "employed"
FROM "sg-data-d-156f700d7c7b3e8ca5d4c1771b15110a"
