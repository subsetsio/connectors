-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "work_week_pattern",
    "distribution"
FROM "sg-data-d-60117eac5efb93aec9943c5c3ef2f51c"
