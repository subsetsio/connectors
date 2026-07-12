-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "male_population",
    "male_population0",
    "female_population",
    "female_population0",
    "total_population",
    "total_population0",
    "annual_growth_rate"
FROM "qatar-planning-and-statistics-authority-total-population-by-sex-in-census-1986-1997-2004-2010-2020"
