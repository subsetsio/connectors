-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "gross_monthly_income_excl_emr_cpf",
    "industry1",
    "industry2",
    "employed"
FROM "sg-data-d-2504fded6f927f7ceb4eb65548ec8068"
