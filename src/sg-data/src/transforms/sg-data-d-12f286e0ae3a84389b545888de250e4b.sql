-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "nmc_course_level",
    "completion_count"
FROM "sg-data-d-12f286e0ae3a84389b545888de250e4b"
