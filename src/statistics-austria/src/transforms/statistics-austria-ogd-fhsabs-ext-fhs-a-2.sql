-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "academic_year",
    "place_of_study",
    "graduations_of_ordinary_studies"
FROM "statistics-austria-ogd-fhsabs-ext-fhs-a-2"
