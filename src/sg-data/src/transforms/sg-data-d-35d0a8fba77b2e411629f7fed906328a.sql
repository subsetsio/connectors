-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Sex" AS sex,
    "Type_of_Abuse" AS type_of_abuse,
    "No_of_non_elderly_VA_cases" AS no_of_non_elderly_va_cases
FROM "sg-data-d-35d0a8fba77b2e411629f7fed906328a"
