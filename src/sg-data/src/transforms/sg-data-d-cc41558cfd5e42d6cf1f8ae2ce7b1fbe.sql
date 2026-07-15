-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "type_of_expenditure",
    "type_of_cost",
    "rnd_expenditure"
FROM "sg-data-d-cc41558cfd5e42d6cf1f8ae2ce7b1fbe"
