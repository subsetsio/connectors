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
    "sheet_name",
    "column_1",
    "column_2",
    "column_3",
    "column_4"
FROM "statsnz-wellbeing-statistics-2023-v2"
