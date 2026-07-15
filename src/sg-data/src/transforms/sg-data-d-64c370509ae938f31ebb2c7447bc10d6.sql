-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "reentry_rate_12mth"
FROM "sg-data-d-64c370509ae938f31ebb2c7447bc10d6"
