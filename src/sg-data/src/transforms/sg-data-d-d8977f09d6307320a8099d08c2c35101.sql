-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age_group",
    "occupation",
    "deaths"
FROM "sg-data-d-d8977f09d6307320a8099d08c2c35101"
