-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "sex1",
    "reentry_rate_6mth"
FROM "sg-data-d-6fa43c0feeb832bf9ffd7257712da9e8"
