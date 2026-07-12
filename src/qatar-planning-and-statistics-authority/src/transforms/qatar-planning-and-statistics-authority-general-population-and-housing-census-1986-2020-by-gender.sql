-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_year",
    "year",
    "general_population_and_housing_census_males",
    "general_population_and_housing_census_females"
FROM "qatar-planning-and-statistics-authority-general-population-and-housing-census-1986-2020-by-gender"
