-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_mobile_subscription"
FROM "sg-data-d-c2b4d1a2c9bfc5d0df58dd339d8121a0"
