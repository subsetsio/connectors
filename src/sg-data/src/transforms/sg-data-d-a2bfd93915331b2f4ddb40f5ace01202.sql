-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Age_Group" AS age_group,
    "Type_of_Abuse" AS type_of_abuse,
    "No_of_child_abuse_cases" AS no_of_child_abuse_cases
FROM "sg-data-d-a2bfd93915331b2f4ddb40f5ace01202"
