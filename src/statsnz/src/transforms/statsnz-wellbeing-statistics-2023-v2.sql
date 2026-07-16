-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "CA_code" AS ca_code,
    "VA_code" AS va_code,
    "estimate",
    "ASE" AS ase,
    "flag",
    "sheet_name" ->> '$' AS sheet_name,
    "column_1" ->> '$' AS codebook_identifier,
    "column_2" ->> '$' AS codebook_variable,
    "column_3" ->> '$' AS codebook_category,
    "column_4" ->> '$' AS codebook_explanation
FROM "statsnz-wellbeing-statistics-2023-v2"
