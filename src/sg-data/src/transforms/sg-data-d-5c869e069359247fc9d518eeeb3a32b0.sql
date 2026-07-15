-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "previous_industry1",
    "previous_industry2",
    "unemployed_with_work_experience"
FROM "sg-data-d-5c869e069359247fc9d518eeeb3a32b0"
