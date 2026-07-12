-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "gender",
    "lnw",
    "percentage_distribution_ltwzy_lnsby",
    "number_of_population_dd_lskn",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-population-by-sex-and-municipality-census-2015"
