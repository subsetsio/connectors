-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "college_nationality",
    "2019_male",
    "2019_female",
    "2019_total",
    "2020_male",
    "2020_female",
    "2020_total",
    "2021_male",
    "2021_female",
    "2021_total",
    "2022_male",
    "2022_female",
    "2022_total",
    "2023_male",
    "2023_female",
    "2023_total",
    "2024_male",
    "2024_female",
    "2024_total"
FROM "qatar-planning-and-statistics-authority-student-enrollment-by-college-and-nationality-2019-2024"
