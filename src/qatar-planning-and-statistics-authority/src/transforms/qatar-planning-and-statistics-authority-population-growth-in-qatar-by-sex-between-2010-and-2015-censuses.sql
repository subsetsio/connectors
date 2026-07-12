-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gender",
    "gender_ar",
    "increase",
    "increase_rate",
    "number_of_population_in_the_censuses"
FROM "qatar-planning-and-statistics-authority-population-growth-in-qatar-by-sex-between-2010-and-2015-censuses"
