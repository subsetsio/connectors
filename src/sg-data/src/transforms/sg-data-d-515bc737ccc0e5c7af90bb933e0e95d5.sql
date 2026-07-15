-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grant_call",
    "awarded_project",
    "recipient",
    "organisation"
FROM "sg-data-d-515bc737ccc0e5c7af90bb933e0e95d5"
