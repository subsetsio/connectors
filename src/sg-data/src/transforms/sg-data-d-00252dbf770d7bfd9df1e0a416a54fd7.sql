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
    "degree_course"
FROM "sg-data-d-00252dbf770d7bfd9df1e0a416a54fd7"
