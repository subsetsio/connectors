-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pipe_diameter_millimetres",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024"
FROM "qatar-planning-and-statistics-authority-length-of-mains-laid-by-year"
