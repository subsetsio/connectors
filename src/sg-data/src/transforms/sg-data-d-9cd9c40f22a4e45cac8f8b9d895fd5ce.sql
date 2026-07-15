-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "median_income_incl_emp_cpf",
    "median_income_excl_emp_cpf"
FROM "sg-data-d-9cd9c40f22a4e45cac8f8b9d895fd5ce"
