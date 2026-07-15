-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "tax_type",
    "no_of_cases",
    "tax_and_penalty_arising"
FROM "sg-data-d-9a018a869f26c830da4d7d239489f9b7"
