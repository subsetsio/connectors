-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "epi_week",
    "disease",
    "no._of_cases" AS no_of_cases
FROM "sg-data-d-5d5508f1c954f5630d7b3aa7875d01f9"
