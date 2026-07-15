-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "previous_occupation",
    "unemployed_with_work_experience"
FROM "sg-data-d-751712fd64b5d061cf3456728734e419"
