-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "industry_code_ANZSIC" AS industry_code_anzsic,
    "industry_name_ANZSIC" AS industry_name_anzsic,
    "rme_size_grp",
    "variable",
    "value",
    "unit",
    "column_8",
    "column_9",
    "column_10",
    "column_11",
    "column_12",
    "column_13",
    "column_14",
    "column_15",
    "column_16"
FROM "statsnz-annual-enterprise-survey-2025-financial-year-provisional-size-bands"
