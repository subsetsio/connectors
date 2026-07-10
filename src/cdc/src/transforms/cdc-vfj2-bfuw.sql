-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week_Ending" AS week_ending,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    "Geography_Name" AS geography_name,
    "Geographic_Level" AS geographic_level,
    CAST("Geography_Name_Order" AS BIGINT) AS geography_name_order,
    CAST("Geography_Label_Sort_Order" AS BIGINT) AS geography_label_sort_order,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    CAST("MMWR_Day" AS BIGINT) AS mmwr_day,
    "Month_Week" AS month_week,
    CAST("Month_Display_Order" AS BIGINT) AS month_display_order,
    CAST("MMWRWeek_Display_Order" AS BIGINT) AS mmwrweek_display_order,
    "Influenza_Season" AS influenza_season,
    "Race_Ethnicity" AS race_ethnicity,
    CAST("Race_Ethnicity_Sort_Order" AS BIGINT) AS race_ethnicity_sort_order,
    CAST("Point_Estimate" AS DOUBLE) AS point_estimate,
    CAST("CI_HalfWidth" AS DOUBLE) AS ci_halfwidth,
    CAST("Lower_CI" AS DOUBLE) AS lower_ci,
    CAST("Upper_CI" AS DOUBLE) AS upper_ci,
    "CI_Range" AS ci_range,
    "Season_Race" AS season_race,
    "Season_Race_Sort_Order" AS season_race_sort_order,
    "Current_Through" AS current_through
FROM "cdc-vfj2-bfuw"
