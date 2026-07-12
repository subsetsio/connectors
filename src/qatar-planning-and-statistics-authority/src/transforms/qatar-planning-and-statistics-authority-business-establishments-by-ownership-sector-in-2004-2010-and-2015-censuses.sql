-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ownership",
    "ownership_ar",
    "2004",
    "2010",
    "2015",
    "annual_increase_rate",
    "increase_rate_during_the_period"
FROM "qatar-planning-and-statistics-authority-business-establishments-by-ownership-sector-in-2004-2010-and-2015-censuses"
