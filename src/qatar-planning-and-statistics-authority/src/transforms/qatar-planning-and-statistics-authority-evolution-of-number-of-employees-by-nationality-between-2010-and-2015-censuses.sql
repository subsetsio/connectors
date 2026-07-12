-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "ljnsy",
    "census_2010_t_dd_2010",
    "census_2015_t_dd_2015",
    "annual_increase_rate",
    "increase",
    "increase_rate_during_the_period"
FROM "qatar-planning-and-statistics-authority-evolution-of-number-of-employees-by-nationality-between-2010-and-2015-censuses"
