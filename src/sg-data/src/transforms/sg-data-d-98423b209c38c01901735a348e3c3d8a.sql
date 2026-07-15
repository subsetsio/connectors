-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "case_type",
    "time_taken",
    "no_of_cases"
FROM "sg-data-d-98423b209c38c01901735a348e3c3d8a"
