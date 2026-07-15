-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_applicant",
    "registration_no",
    "registration_no_alphabet",
    "handphone_no",
    "home_tel",
    "office_tel"
FROM "sg-data-d-2a0bee4473e1d1d8635b4e63e2279eb9"
