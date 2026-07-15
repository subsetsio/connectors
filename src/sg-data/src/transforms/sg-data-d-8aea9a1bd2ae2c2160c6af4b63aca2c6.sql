-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "total_paid_hours",
    "standard_hours"
FROM "sg-data-d-8aea9a1bd2ae2c2160c6af4b63aca2c6"
