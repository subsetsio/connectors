-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "industry1",
    "industry2",
    "age",
    "employed"
FROM "sg-data-d-a7ece9330c024a90b258776e69c2ae00"
