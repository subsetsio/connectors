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
    "column_10" AS extra_year,
    "column_11" AS extra_industry_code_anzsic,
    "column_12" AS extra_industry_name_anzsic,
    "column_13" AS extra_rme_size_grp,
    "column_14" AS extra_variable,
    "column_15" AS extra_value,
    "column_16" AS extra_unit
FROM "statsnz-annual-enterprise-survey-2025-financial-year-provisional-size-bands"
