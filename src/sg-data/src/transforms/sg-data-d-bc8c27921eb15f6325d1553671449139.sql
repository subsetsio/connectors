-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Age_Group" AS age_group,
    "Sex" AS sex,
    "No_of_self_neglect_cases" AS no_of_self_neglect_cases
FROM "sg-data-d-bc8c27921eb15f6325d1553671449139"
