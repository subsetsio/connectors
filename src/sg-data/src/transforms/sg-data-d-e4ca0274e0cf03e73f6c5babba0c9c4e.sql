-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "half_year",
    "type",
    "number"
FROM "sg-data-d-e4ca0274e0cf03e73f6c5babba0c9c4e"
