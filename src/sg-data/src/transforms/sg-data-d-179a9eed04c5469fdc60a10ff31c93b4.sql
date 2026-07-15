-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "reentry_rate_6mth"
FROM "sg-data-d-179a9eed04c5469fdc60a10ff31c93b4"
