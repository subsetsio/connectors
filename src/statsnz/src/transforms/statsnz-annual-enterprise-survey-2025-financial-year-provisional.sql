-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Year" AS BIGINT) AS year,
    "Industry_aggregation_NZSIOC" AS industry_aggregation_nzsioc,
    "Industry_code_NZSIOC" AS industry_code_nzsioc,
    "Industry_name_NZSIOC" AS industry_name_nzsioc,
    "Units" AS units,
    "Variable_code" AS variable_code,
    "Variable_name" AS variable_name,
    "Variable_category" AS variable_category,
    "Value" AS value,
    "Industry_code_ANZSIC06" AS industry_code_anzsic06
FROM "statsnz-annual-enterprise-survey-2025-financial-year-provisional"
