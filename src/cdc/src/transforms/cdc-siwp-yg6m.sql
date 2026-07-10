-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Year" AS year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week-Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "Jurisdiction of Occurrence" AS jurisdiction_of_occurrence,
    "Race and Hispanic Origin Group" AS race_and_hispanic_origin_group,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths
FROM "cdc-siwp-yg6m"
