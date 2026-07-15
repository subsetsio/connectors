-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_case_type",
    "subcategory",
    "count"
FROM "sg-data-d-111ef64ac94ff53a44f5e019b8ed9878"
