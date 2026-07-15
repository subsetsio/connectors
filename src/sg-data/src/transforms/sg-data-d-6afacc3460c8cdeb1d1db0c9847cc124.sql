-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "marital_status",
    "age",
    "outside_labour_force"
FROM "sg-data-d-6afacc3460c8cdeb1d1db0c9847cc124"
