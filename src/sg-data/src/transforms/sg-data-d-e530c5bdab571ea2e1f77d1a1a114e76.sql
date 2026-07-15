-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "max_laden_wt",
    "type",
    "number"
FROM "sg-data-d-e530c5bdab571ea2e1f77d1a1a114e76"
