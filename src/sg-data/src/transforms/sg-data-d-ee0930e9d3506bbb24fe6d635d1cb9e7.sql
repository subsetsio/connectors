-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_by_gender",
    "number_of_population"
FROM "sg-data-d-ee0930e9d3506bbb24fe6d635d1cb9e7"
