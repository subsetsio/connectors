-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "lnw",
    "census_2015_t_dd_2015",
    "census_2010_t_dd_2010",
    "increase",
    "increase_rate_during_the_period",
    "annual_increase_rate"
FROM "qatar-planning-and-statistics-authority-number-of-non-qatari-employees-in-business-establishments-by-sex-in-2010-and-2015-censuses"
