-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "type",
    "category",
    "number"
FROM "sg-data-d-11af4cacfdd459f8712fb903b1639d98"
