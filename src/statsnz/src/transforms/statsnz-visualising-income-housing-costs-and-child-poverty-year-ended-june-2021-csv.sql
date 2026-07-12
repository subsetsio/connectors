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
    "MsCode" AS mscode,
    CAST("Year" AS BIGINT) AS year,
    "EstCode" AS estcode,
    "Estimate" AS estimate,
    "SE" AS se,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag,
    "DemCode" AS demcode
FROM "statsnz-visualising-income-housing-costs-and-child-poverty-year-ended-june-2021-csv"
