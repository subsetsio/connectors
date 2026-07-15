-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no_of_accounts",
    "total_balance",
    "average_balance",
    "amount_withdrawn"
FROM "sg-data-d-2ed23324aeac97609c4e16299ab05ffc"
