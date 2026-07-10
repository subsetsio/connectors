-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "semester",
    "type_of_study",
    "all_students"
FROM "statistics-austria-ogd-unistud2-ext-uni-stud2-1"
