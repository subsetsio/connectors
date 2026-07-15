-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "case_type",
    "status",
    "no_of_cases"
FROM "sg-data-d-f16f93f9c1a7f2ce8f466724fc2a6579"
