-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "academic_year",
    "federal_country_province",
    "type_of_teacher",
    "number_of_teaching_staff",
    "full_time_equivalent"
FROM "statistics-austria-ogd-persph-lehr-1"
