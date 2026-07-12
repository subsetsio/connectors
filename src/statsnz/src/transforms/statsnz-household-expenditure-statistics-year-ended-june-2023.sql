-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "column_1",
    "column_2",
    "column_3",
    "column_4",
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
