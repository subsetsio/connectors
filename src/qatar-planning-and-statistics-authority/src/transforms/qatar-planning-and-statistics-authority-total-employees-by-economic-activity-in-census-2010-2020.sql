-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity",
    "lnsht_lqtsdy",
    "census_2020_2020",
    "2020_census_2020",
    "census_2010_2010",
    "2010_census_2010",
    "change"
FROM "qatar-planning-and-statistics-authority-total-employees-by-economic-activity-in-census-2010-2020"
