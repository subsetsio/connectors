-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_products",
    "percentage"
FROM "sg-data-d-dec34f3ed7daeb6429c8d8b7c36852d2"
