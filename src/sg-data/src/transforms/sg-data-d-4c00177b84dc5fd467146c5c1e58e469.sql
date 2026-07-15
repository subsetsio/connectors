-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "nmc_course_level",
    "graduate_count"
FROM "sg-data-d-4c00177b84dc5fd467146c5c1e58e469"
