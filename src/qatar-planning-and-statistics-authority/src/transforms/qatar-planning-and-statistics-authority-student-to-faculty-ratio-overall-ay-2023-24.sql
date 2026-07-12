-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "student_fte",
    "faculty_count",
    "student_faculty_ratio"
FROM "qatar-planning-and-statistics-authority-student-to-faculty-ratio-overall-ay-2023-24"
