-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "2021_2022",
    "2022_2023",
    "2023_2024"
FROM "qatar-planning-and-statistics-authority-number-of-graduates-by-age-group-and-academic-year"
