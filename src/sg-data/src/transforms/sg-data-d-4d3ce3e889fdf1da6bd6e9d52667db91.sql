-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "reentry_rate_6mth"
FROM "sg-data-d-4d3ce3e889fdf1da6bd6e9d52667db91"
