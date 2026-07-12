-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "2024_2023",
    "2023_2022",
    "2022_2021",
    "2021_2020",
    "2020_2019",
    "2019_2018",
    "2018_2017",
    "2017_2016"
FROM "qatar-planning-and-statistics-authority-the-number-of-students-who-are-citizens-of-the-gcc-countries-enrolled-in-government-higher-education"
