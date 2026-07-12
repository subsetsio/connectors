-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "census_year",
    "age_group",
    "male_population",
    "male_population0",
    "female_population",
    "female_population0",
    "total_population",
    "total_population0",
    "sex_ratio"
FROM "qatar-planning-and-statistics-authority-total-population-by-age-groups-and-sex-in-census-2010-2020"
