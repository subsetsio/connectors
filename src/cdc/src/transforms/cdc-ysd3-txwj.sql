-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Cumulative_Doses" AS BIGINT) AS cumulative_doses,
    "Influenza_Season" AS influenza_season,
    "Setting" AS setting,
    "Week_ID" AS week_id,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    CAST("MMWR_Week_Order" AS BIGINT) AS mmwr_week_order,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    CAST("MMWR_Day" AS BIGINT) AS mmwr_day,
    CAST("Doses" AS BIGINT) AS doses,
    "Current_Through" AS current_through,
    CAST("Location_and_Flu_Season_Order" AS BIGINT) AS location_and_flu_season_order,
    "Age_Group" AS age_group
FROM "cdc-ysd3-txwj"
