-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_type",
    "financial_scheme",
    "eligibility",
    "award",
    "reference"
FROM "sg-data-d-f98b0d0bf644c30ce95129f95a947b9c"
