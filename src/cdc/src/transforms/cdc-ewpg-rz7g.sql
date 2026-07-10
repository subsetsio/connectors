-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "COVID-19_Season" AS covid_19_season,
    "Week_ID" AS week_id,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    CAST("MMWR_Week_Order" AS BIGINT) AS mmwr_week_order,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    CAST("MMWR_Day" AS BIGINT) AS mmwr_day,
    "Setting" AS setting,
    CAST("Doses" AS BIGINT) AS doses,
    CAST("Cumulative_Doses" AS BIGINT) AS cumulative_doses,
    CAST("Location_and_Flu_Season_Order" AS BIGINT) AS location_and_flu_season_order,
    "Current_Through" AS current_through,
    "Age_Group" AS age_group
FROM "cdc-ewpg-rz7g"
