-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "census_type",
    "nw_lt_dd",
    "census_2010_t_dd_2010",
    "census_2015_t_dd_2015",
    "increase",
    "annual_increase_rate",
    "increase_rate_during_the_period"
FROM "qatar-planning-and-statistics-authority-growth-of-business-establishments-and-employees-in-census-2010-compared-to-census-2015"
