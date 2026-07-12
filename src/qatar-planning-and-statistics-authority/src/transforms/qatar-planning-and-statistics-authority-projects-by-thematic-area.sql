-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "subject_area",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-projects-by-thematic-area"
