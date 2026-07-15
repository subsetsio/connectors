-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "age1",
    "reentry_rate_6mth"
FROM "sg-data-d-9548bb2124143f77b76c51ee8c895b69"
