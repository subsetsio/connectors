-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "number_of_population_dd_lskn",
    "percentage_distribution_ltwzy_lnsby",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-population-by-municipalities-in-qatar-between-2010-and-2015-censuses"
