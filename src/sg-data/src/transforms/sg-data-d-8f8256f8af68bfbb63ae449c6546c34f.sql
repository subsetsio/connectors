-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "stream",
    "LEVEL" AS level,
    "ENROLMENT" AS enrolment
FROM "sg-data-d-8f8256f8af68bfbb63ae449c6546c34f"
