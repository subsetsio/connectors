-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "training_seats",
    "unique_learners"
FROM "qatar-planning-and-statistics-authority-participation-at-qatar-digital-academy-by-gender-2024"
