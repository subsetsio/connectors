-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "type_of_space",
    "availability",
    "amount_of_space"
FROM "sg-data-d-d23a8c26d4a9530d651fbe0248a3f1fc"
