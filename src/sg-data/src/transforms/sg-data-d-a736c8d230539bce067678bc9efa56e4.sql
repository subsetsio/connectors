-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_employee",
    "annual_leave_entitlement",
    "distribution"
FROM "sg-data-d-a736c8d230539bce067678bc9efa56e4"
