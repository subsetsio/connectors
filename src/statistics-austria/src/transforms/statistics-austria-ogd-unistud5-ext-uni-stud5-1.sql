-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "semester",
    "students",
    "ordinary_students",
    "students_of_courses_of_studies_lehrgang",
    "new_entrants"
FROM "statistics-austria-ogd-unistud5-ext-uni-stud5-1"
