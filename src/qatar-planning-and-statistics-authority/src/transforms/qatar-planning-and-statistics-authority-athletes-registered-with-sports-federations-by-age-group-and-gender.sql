-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "adults_male",
    "adults_female",
    "youth_male",
    "youth_female",
    "junior_18_male",
    "junior_18_female",
    "junior_16_male",
    "junior_16_female",
    "kids_male",
    "kids_female",
    "total_male",
    "total_female",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-athletes-registered-with-sports-federations-by-age-group-and-gender"
