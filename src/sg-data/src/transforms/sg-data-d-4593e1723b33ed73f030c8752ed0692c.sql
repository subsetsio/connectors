-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Age_Group" AS age_group,
    "Sex" AS sex,
    "No_of_child_abuse_cases" AS no_of_child_abuse_cases
FROM "sg-data-d-4593e1723b33ed73f030c8752ed0692c"
