-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week Ending" AS week_ending,
    "COVID-19_Season" AS covid_19_season,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("MMWR_Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR_Week" AS BIGINT) AS mmwr_week,
    "Enrollment Date" AS enrollment_date,
    "As of date" AS as_of_date,
    "Race and ethnicity" AS race_and_ethnicity,
    CAST("Current_Season_Week_Ending_Label" AS TIMESTAMP) AS current_season_week_ending_label
FROM "cdc-jjpx-mxt8"
