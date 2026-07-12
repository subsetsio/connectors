-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "usage",
    "value_cubic_metre_year_per_capita"
FROM "qatar-planning-and-statistics-authority-per-capita-water-consumption-for-different-usages-m3-year-per-capita"
