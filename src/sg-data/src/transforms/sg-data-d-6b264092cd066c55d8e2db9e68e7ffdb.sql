-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "course",
    "intake",
    "enrolment",
    "graduates"
FROM "sg-data-d-6b264092cd066c55d8e2db9e68e7ffdb"
