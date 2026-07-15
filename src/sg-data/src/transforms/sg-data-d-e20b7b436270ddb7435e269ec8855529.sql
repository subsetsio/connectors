-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "highest_qualification",
    "unemployed"
FROM "sg-data-d-e20b7b436270ddb7435e269ec8855529"
