-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Age_Group" AS age_group,
    "Type_of_Abuse" AS type_of_abuse,
    "No_of_non_elderly_VA_cases" AS no_of_non_elderly_va_cases
FROM "sg-data-d-bce95b79ba198c25b078784063c79ab5"
