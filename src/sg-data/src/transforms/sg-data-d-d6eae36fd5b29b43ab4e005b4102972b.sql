-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "intake",
    "enrolment",
    "graduates",
    "diploma_course"
FROM "sg-data-d-d6eae36fd5b29b43ab4e005b4102972b"
