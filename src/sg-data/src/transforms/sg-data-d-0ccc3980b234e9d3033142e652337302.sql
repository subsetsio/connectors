-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "education1",
    "reentry_rate_12mth"
FROM "sg-data-d-0ccc3980b234e9d3033142e652337302"
