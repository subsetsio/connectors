-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegNo" AS regno,
    "Name" AS name,
    "Practice_Employer_Name" AS practice_employer_name,
    "Practice_Employer_Type" AS practice_employer_type,
    "Period_of_Suspension" AS period_of_suspension
FROM "sg-data-d-662d69b0919fc752a43175eb178030d5"
