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
FROM "sg-data-d-c37a83ab34cdb0a732a40415cbf33c3a"
