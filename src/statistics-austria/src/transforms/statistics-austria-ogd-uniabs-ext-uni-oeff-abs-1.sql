-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "academic_year",
    "graduations_of_ordinary_studies"
FROM "statistics-austria-ogd-uniabs-ext-uni-oeff-abs-1"
