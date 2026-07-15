-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_reason_for_not_working",
    "distribution_of_pwd_by_main_reason_for_not_working"
FROM "sg-data-d-3549a6a5fb5cfff7eae662b946857760"
