-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "column_1" AS codebook_identifier,
    "column_2" AS codebook_variable,
    "column_3" AS codebook_category,
    "column_4" AS codebook_explanation,
    "MsCode" AS mscode,
    CAST("Year" AS BIGINT) AS year,
    "EstCode" AS estcode,
    "Estimate" AS estimate,
    "SE" AS se,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag,
    "DemCode" AS demcode
FROM "statsnz-child-poverty-statistics-year-ended-june-2025"
