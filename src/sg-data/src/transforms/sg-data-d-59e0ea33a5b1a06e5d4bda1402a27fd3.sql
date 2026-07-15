-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "tax_group",
    "income_type",
    "amount"
FROM "sg-data-d-59e0ea33a5b1a06e5d4bda1402a27fd3"
