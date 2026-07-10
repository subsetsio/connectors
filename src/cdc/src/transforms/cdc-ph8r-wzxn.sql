-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Influenza_Season" AS influenza_season,
    "Start_Date" AS start_date,
    "End_Date" AS end_date,
    "Reporting_TimeFrame" AS reporting_timeframe,
    CAST("Week_Sort_Order" AS BIGINT) AS week_sort_order,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    CAST("Cumulative_Flu_Doses_Distributed" AS DOUBLE) AS cumulative_flu_doses_distributed,
    "Current_Through" AS current_through
FROM "cdc-ph8r-wzxn"
