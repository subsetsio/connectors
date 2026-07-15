-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegNo" AS regno,
    "Name" AS name,
    "Employer" AS employer,
    "BranchofEngineering" AS branchofengineering,
    "DateofRegistration" AS dateofregistration
FROM "sg-data-d-50c58ff1ca87758b8adc2cadd66d60b9"
