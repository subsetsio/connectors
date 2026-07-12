-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sport_facility",
    "sport_facility_ar",
    "2018_2019",
    "2019_2020",
    "2020_2021",
    "2021_2022"
FROM "qatar-planning-and-statistics-authority-sport-facilities-by-type-2018-2022"
