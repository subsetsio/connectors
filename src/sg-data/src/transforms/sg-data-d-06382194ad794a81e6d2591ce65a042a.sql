-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "sex1",
    "reentry_rate_12mth"
FROM "sg-data-d-06382194ad794a81e6d2591ce65a042a"
