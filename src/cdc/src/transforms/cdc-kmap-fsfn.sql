-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data_Collection_Start_Date" AS data_collection_start_date,
    "Data_Collection_End_Date" AS data_collection_end_date,
    "Data_Collection_Midpoint_date" AS data_collection_midpoint_date,
    CAST("Data_Collection_Midpoint_MMWR_Year" AS BIGINT) AS data_collection_midpoint_mmwr_year,
    CAST("Data_Collection_Midpoint_MMWR_Week" AS BIGINT) AS data_collection_midpoint_mmwr_week,
    CAST("Data_Collection_Midpoint_MMWR_Day" AS BIGINT) AS data_collection_midpoint_mmwr_day,
    CAST("Data_Collection_Midpoint_MMWRWeek_Display_Order" AS BIGINT) AS data_collection_midpoint_mmwrweek_display_order,
    "Month_Abbrev" AS month_abbrev,
    CAST("Month_Sort_Order" AS BIGINT) AS month_sort_order,
    "Data_Source" AS data_source,
    CAST("Suppressed" AS BOOLEAN) AS suppressed,
    "Race_Ethnicity" AS race_ethnicity,
    "Age_Group" AS age_group,
    CAST("Point_Estimate" AS DOUBLE) AS point_estimate,
    CAST("CI_HalfWidth" AS DOUBLE) AS ci_halfwidth,
    CAST("CI_Lower" AS DOUBLE) AS ci_lower,
    CAST("CI_Upper" AS DOUBLE) AS ci_upper,
    "Sample_Size" AS sample_size
FROM "cdc-kmap-fsfn"
