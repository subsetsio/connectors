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
    "Table" AS table,
    "Year" AS year,
    "MsCode" AS mscode,
    "CatCode" AS catcode,
    "HECCode" AS heccode,
    "Estimate" AS estimate,
    "RSE" AS rse,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag
FROM "statsnz-household-expenditure-statistics-year-ended-june-2023"
