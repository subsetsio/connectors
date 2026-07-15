-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "no_of_cases",
    "tax_and_penalty_arising"
FROM "sg-data-d-c22092e14ddf8976d49024c2e642abad"
