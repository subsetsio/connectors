-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "level_of_school",
    "age",
    "no_of_teachers"
FROM "sg-data-d-3903d6f48227cf4a87a346b7f4958aa9"
