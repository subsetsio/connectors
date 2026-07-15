-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "account_type",
    "net_amt"
FROM "sg-data-d-ac6e9a81c38da6cd1cd4c66ec72f16f4"
