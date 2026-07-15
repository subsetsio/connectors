-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_education_level",
    "number_of_population"
FROM "sg-data-d-bd8146bb208b9beb22b9bd62c61fa0e1"
