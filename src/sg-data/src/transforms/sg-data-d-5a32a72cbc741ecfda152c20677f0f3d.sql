-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "category",
    "type",
    "number"
FROM "sg-data-d-5a32a72cbc741ecfda152c20677f0f3d"
