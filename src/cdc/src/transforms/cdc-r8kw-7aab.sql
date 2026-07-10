-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data as of" AS data_as_of,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Group" AS group,
    "Year" AS year,
    CAST("Month" AS BIGINT) AS month,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "State" AS state,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("Percent of Expected Deaths" AS BIGINT) AS percent_of_expected_deaths,
    CAST("Pneumonia Deaths" AS BIGINT) AS pneumonia_deaths,
    CAST("Pneumonia and COVID-19 Deaths" AS BIGINT) AS pneumonia_and_covid_19_deaths,
    CAST("Influenza Deaths" AS BIGINT) AS influenza_deaths,
    CAST("Pneumonia, Influenza, or COVID-19 Deaths" AS BIGINT) AS pneumonia_influenza_or_covid_19_deaths,
    "Footnote" AS footnote
FROM "cdc-r8kw-7aab"
