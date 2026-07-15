-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "issuance_date",
    "maturity_date",
    "credit_rating",
    "bond_coupon",
    "bond_amount"
FROM "sg-data-d-83ff203724fe94184ae5c172f26942e0"
