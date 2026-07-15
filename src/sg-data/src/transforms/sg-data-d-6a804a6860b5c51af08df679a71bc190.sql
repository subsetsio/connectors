-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "actual_revised_estimated",
    "type",
    "category",
    "class",
    "amount"
FROM "sg-data-d-6a804a6860b5c51af08df679a71bc190"
