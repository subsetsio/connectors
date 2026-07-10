-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    strptime("Start Week", '%m/%d/%Y')::DATE AS start_week,
    strptime("End Week", '%m/%d/%Y')::DATE AS end_week,
    CAST("MMWRyear" AS BIGINT) AS mmwryear,
    CAST("MMWRweek" AS BIGINT) AS mmwrweek,
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "Group" AS group,
    "Indicator" AS indicator,
    "Jurisdiction" AS jurisdiction,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("Pneumonia Deaths" AS BIGINT) AS pneumonia_deaths,
    CAST("Influenza Deaths" AS BIGINT) AS influenza_deaths,
    CAST("Pneumonia or Influenza" AS BIGINT) AS pneumonia_or_influenza,
    CAST("Pneumonia, Influenza, or COVID-19 Deaths" AS BIGINT) AS pneumonia_influenza_or_covid_19_deaths,
    "Footnote" AS footnote
FROM "cdc-ynw2-4viq"
