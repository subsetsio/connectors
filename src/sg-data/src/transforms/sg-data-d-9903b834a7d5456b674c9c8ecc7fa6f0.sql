-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "no_of_trade_disputes"
FROM "sg-data-d-9903b834a7d5456b674c9c8ecc7fa6f0"
