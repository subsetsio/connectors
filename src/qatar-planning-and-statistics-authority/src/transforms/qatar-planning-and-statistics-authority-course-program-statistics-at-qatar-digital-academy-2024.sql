-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_type",
    "courses_offered",
    "training_seats",
    "unique_participants"
FROM "qatar-planning-and-statistics-authority-course-program-statistics-at-qatar-digital-academy-2024"
