-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_disability",
    "type_of_disability_ar",
    "adults_males",
    "adults_females",
    "youth_males",
    "youth_females",
    "junior_under_18_males",
    "junior_under_18_females",
    "junior_under_16_males",
    "junior_under_16_females",
    "kids_males",
    "kids_females"
FROM "qatar-planning-and-statistics-authority-athletes-registered-with-disabled-sports-federation-by-type-of-disability-age-groups-and-gender-2021"
