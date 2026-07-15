-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Sex" AS sex,
    "Type_of_Abuse" AS type_of_abuse,
    "No_of_child_abuse_cases" AS no_of_child_abuse_cases
FROM "sg-data-d-0e83a60152fd6e5a3a763a27ff41a71f"
