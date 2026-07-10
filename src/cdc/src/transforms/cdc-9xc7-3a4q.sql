-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Group" AS group,
    "Year" AS year,
    CAST("Month" AS BIGINT) AS month,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week-Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    CAST("HHS Region" AS BIGINT) AS hhs_region,
    "Race and Hispanic Origin Group" AS race_and_hispanic_origin_group,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    "Footnote" AS footnote
FROM "cdc-9xc7-3a4q"
