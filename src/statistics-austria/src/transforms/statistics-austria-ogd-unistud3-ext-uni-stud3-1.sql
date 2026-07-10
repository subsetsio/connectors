-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "semester",
    "university",
    "all_students_per_university"
FROM "statistics-austria-ogd-unistud3-ext-uni-stud3-1"
