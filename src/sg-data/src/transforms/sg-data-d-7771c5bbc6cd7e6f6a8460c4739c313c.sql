-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "sex",
    "enrolment_primary"
FROM "sg-data-d-7771c5bbc6cd7e6f6a8460c4739c313c"
