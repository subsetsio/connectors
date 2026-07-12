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
    CAST(NULL AS VARCHAR) AS sheet_name,
    CAST(NULL AS VARCHAR) AS column_1,
    CAST(NULL AS VARCHAR) AS column_2,
    CAST(NULL AS VARCHAR) AS column_3,
    CAST(NULL AS VARCHAR) AS column_4
FROM "statsnz-wellbeing-statistics-2023-v2"
