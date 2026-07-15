-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "YEAR" AS year,
    "LEVEL" AS level,
    "AGE" AS age,
    "SEX" AS sex,
    "ENROLMENT" AS enrolment
FROM "sg-data-d-cc84fc751ef5106d9e26cfdbf61776c8"
