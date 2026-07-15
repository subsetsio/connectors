-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_age_group",
    "number_of_population"
FROM "sg-data-d-f8cf15f013db8a073982514a0eb95876"
