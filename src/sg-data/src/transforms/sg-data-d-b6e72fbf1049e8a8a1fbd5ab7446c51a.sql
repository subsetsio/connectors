-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex1",
    "reentry_rate_6mth"
FROM "sg-data-d-b6e72fbf1049e8a8a1fbd5ab7446c51a"
