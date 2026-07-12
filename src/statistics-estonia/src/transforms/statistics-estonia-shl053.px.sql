-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "change_in_the_number_of_chronic_diseases",
    "indicator",
    "birth_cohort",
    "sex",
    "value"
FROM "statistics-estonia-shl053.px"
