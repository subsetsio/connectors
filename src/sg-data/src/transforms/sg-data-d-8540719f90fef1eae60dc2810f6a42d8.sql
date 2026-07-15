-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "registration_no",
    "name"
FROM "sg-data-d-8540719f90fef1eae60dc2810f6a42d8"
