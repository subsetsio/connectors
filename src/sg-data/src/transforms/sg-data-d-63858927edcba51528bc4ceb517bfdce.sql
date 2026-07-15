-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "case_type",
    "no_completed_cases",
    "financial_year"
FROM "sg-data-d-63858927edcba51528bc4ceb517bfdce"
