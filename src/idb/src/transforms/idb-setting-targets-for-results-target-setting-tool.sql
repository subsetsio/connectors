-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicators" AS indicators,
    "Unit_Value_vi" AS unit_value_vi,
    CAST("Value_20_yrs_horizon_12%_discount_rate" AS DOUBLE) AS value_20_yrs_horizon_12_discount_rate,
    CAST("Target_Population" AS DOUBLE) AS target_population,
    CAST("Length_of_program_in_years" AS BIGINT) AS length_of_program_in_years,
    CAST("Total_Cost" AS BIGINT) AS total_cost,
    CAST("2008_Level" AS DOUBLE) AS 2008_level,
    CAST("2011_level" AS DOUBLE) AS 2011_level,
    "2011_Level_95%_CI" AS 2011_level_95_ci,
    CAST("Trend" AS DOUBLE) AS trend,
    CAST("Estimated_Targets" AS DOUBLE) AS estimated_targets,
    "source_resource"
FROM "idb-setting-targets-for-results-target-setting-tool"
