-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week_Ending" AS week_ending,
    "Influenza_Season" AS influenza_season,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    CAST("MMWR_Day" AS BIGINT) AS mmwr_day,
    CAST("MMWRWeek_Display_Order" AS BIGINT) AS mmwrweek_display_order,
    "Race_Ethnicity" AS race_ethnicity,
    CAST("Point_Estimate" AS DOUBLE) AS point_estimate,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label
FROM "cdc-g57i-yx3r"
