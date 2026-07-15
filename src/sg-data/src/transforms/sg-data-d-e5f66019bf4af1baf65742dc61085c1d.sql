-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "fundingtype",
    "amount"
FROM "sg-data-d-e5f66019bf4af1baf65742dc61085c1d"
