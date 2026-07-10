-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "semester",
    "studies_of_lehramt_to_become_a_teacher",
    "courses_of_studies_lehrgang",
    "newly_enrolled_studies_of_lehramt",
    "newly_enrolled_courses_of_studies_lehrgang"
FROM "statistics-austria-ogd-phsstud-ext-phs-s-1"
