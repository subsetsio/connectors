-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "academic_year",
    "graduations_of_ordinary_studies",
    "graduations_of_courses_of_studies_lehrgang"
FROM "statistics-austria-ogd-fhsabs-ext-fhs-a-1"
