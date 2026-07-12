-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity",
    "economic_activity_ar",
    "census_2020",
    "percent_census_2020",
    "census_2010_2010",
    "percent_census_2010",
    "percent_change"
FROM "qatar-planning-and-statistics-authority-number-of-business-establishments-by-economic-activity-in-census-2010-2020"
