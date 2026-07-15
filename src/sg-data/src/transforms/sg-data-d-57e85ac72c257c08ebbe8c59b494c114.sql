-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_type",
    "financial_scheme",
    "eligibility",
    "award_quantum_condition",
    "reference"
FROM "sg-data-d-57e85ac72c257c08ebbe8c59b494c114"
