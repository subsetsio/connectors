-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "case_number",
    "outcome_of_cases"
FROM "sg-data-d-78b6f3b7151f01bab5740ddfe2f1b5f4"
