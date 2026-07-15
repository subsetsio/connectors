-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "drug",
    "unit_of_measure",
    "amount"
FROM "sg-data-d-548c4312b99409c9d152ac2f426828b5"
