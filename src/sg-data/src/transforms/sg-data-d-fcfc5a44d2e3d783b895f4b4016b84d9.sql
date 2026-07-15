-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "age",
    "occupation",
    "percentage"
FROM "sg-data-d-fcfc5a44d2e3d783b895f4b4016b84d9"
