-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "category",
    "number"
FROM "sg-data-d-f8876e8c0959ba5bcfa2c40cf6d25dab"
