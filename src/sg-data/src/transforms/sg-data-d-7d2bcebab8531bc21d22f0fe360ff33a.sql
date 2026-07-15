-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "duration_of_unemployment",
    "unemployed"
FROM "sg-data-d-7d2bcebab8531bc21d22f0fe360ff33a"
