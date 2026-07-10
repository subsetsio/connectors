-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    CAST("Month" AS BIGINT) AS month,
    "HHS_Region" AS hhs_region,
    "Pathogen" AS pathogen,
    CAST("Number_of_isolates" AS BIGINT) AS number_of_isolates,
    CAST("Past_two_years_average" AS DOUBLE) AS past_two_years_average
FROM "cdc-khic-yj26"
