-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "adults_m",
    "adults_f",
    "youth_m",
    "youth_f",
    "u18_m",
    "u18_f",
    "u16_m",
    "u16_f",
    "kids_m",
    "kids_f",
    "total_m",
    "total_f",
    "total"
FROM "qatar-planning-and-statistics-authority-athletes-registered-in-sports-federations-by-sports-activity-age-groups-and-gender-2023"
