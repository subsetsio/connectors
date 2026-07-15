-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Age_Group" AS age_group,
    "Sex" AS sex,
    "No_of_non_elderly_VA_cases" AS no_of_non_elderly_va_cases
FROM "sg-data-d-0d08a4ca61abb6bce2291f359b047808"
