-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "category",
    "no_of_units"
FROM "sg-data-d-007b79018e47094e8cd62bf6f6d9ed8e"
