-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "StatCode" AS statcode,
    "MsCode" AS mscode,
    CAST("year" AS BIGINT) AS year,
    "Estimate" AS estimate,
    "SE" AS se,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag,
    "column_9",
    "column_10",
    "column_11",
    "PerCode" AS percode,
    "DwCode" AS dwcode,
    CAST("Year_1" AS BIGINT) AS year_1,
    "RegCode" AS regcode,
    "RSE" AS rse,
    "QuintCode" AS quintcode,
    "EstCode" AS estcode,
    "IncCode" AS inccode,
    "HdCode" AS hdcode,
    "PdCode" AS pdcode,
    "ExpCode" AS expcode,
    "sheet_name",
    "column_1",
    "column_2",
    "column_3",
    "column_4"
FROM "statsnz-household-income-and-housing-cost-statistics-year-ended-june-2025-corrected"
