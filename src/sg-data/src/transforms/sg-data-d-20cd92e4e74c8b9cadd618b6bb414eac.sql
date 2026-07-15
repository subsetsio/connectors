-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "sex",
    "enrolment_secondary"
FROM "sg-data-d-20cd92e4e74c8b9cadd618b6bb414eac"
