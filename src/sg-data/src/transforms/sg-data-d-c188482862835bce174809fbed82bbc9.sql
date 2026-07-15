-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "level_of_school",
    "age",
    "no_of_vice_principals"
FROM "sg-data-d-c188482862835bce174809fbed82bbc9"
