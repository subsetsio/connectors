-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "adults_males",
    "adults_females",
    "youth_males",
    "youth_females",
    "junior_u18_males",
    "junior_u18_females",
    "junior_u16_males",
    "junior_u16_females",
    "kids_males",
    "kids_females"
FROM "qatar-planning-and-statistics-authority-athletes-registered-with-sports-federations-by-sports-activity-age-groups-and-gender-2021-2022"
