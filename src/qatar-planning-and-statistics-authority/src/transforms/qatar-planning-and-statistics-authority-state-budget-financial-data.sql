-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_ar",
    "actual_2021_ar",
    "actual_2022_ar",
    "actual_2023_ar",
    "actual_2024_ar",
    "budgeted_2025_ar",
    "notes_ar"
FROM "qatar-planning-and-statistics-authority-state-budget-financial-data"
