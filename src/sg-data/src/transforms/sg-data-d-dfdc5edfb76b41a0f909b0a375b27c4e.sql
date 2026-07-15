-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_gender",
    "number_of_population"
FROM "sg-data-d-dfdc5edfb76b41a0f909b0a375b27c4e"
