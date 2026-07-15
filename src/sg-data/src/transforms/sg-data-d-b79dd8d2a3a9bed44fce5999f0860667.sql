-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "full_time_graduates",
    "part_time_graduates",
    "total"
FROM "sg-data-d-b79dd8d2a3a9bed44fce5999f0860667"
