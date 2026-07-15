-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_education_level",
    "number_of_population"
FROM "sg-data-d-949f02d8e5f54488a5d6a48a6d9f5e50"
