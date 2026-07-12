-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Table" AS table,
    "AsCode" AS ascode,
    "Demcode" AS demcode,
    CAST("Year" AS BIGINT) AS year,
    "EstCode" AS estcode,
    "Estimate" AS estimate,
    "SE" AS se,
    "LowerCIB" AS lowercib,
    "UpperCIB" AS uppercib,
    "Flag" AS flag
FROM "statsnz-household-net-worth-statistics-year-ended-june-2024"
