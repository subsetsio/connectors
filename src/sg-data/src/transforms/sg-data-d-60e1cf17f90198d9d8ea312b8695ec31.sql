-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation1",
    "reentry_rate_6mth"
FROM "sg-data-d-60e1cf17f90198d9d8ea312b8695ec31"
