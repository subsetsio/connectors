-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "facility",
    "number"
FROM "sg-data-d-778e6d2eaf4a3812aab0d1a1bdf7fd38"
