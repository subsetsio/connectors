-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "category",
    "type",
    "number"
FROM "sg-data-d-b876ece1b4a3bb5ebdc33c4394a236a2"
