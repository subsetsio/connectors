-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "education_level",
    "sex",
    "citizenship_category",
    "first_language",
    "year",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1502010000-101"
