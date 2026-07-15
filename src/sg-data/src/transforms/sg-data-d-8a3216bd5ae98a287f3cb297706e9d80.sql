-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type",
    "age",
    "number_reported",
    "number_passed",
    "passing_rate"
FROM "sg-data-d-8a3216bd5ae98a287f3cb297706e9d80"
