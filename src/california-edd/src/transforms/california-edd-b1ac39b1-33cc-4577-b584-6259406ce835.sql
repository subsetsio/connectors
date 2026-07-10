-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-term industry projections mix areas and NAICS hierarchy levels; filter area and NAICS level before aggregating projected employment.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Period" AS period,
    "NAICS Level" AS naics_level,
    "NAICS Code" AS naics_code,
    "Industry Title" AS industry_title,
    CAST("Base Year Employment Estimate" AS BIGINT) AS base_year_employment_estimate,
    CAST("Projected Year Employment Estimate" AS BIGINT) AS projected_year_employment_estimate,
    CAST("Numeric Change" AS BIGINT) AS numeric_change,
    CAST("Percentage Change" AS DOUBLE) AS percentage_change
FROM "california-edd-b1ac39b1-33cc-4577-b584-6259406ce835"
