-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Group" AS group,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "State" AS state,
    "Sex" AS sex,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("Pneumonia Deaths" AS BIGINT) AS pneumonia_deaths,
    CAST("Pneumonia and COVID-19 Deaths" AS BIGINT) AS pneumonia_and_covid_19_deaths,
    CAST("Influenza Deaths" AS BIGINT) AS influenza_deaths,
    CAST("Pneumonia, Influenza, or COVID-19 Deaths" AS BIGINT) AS pneumonia_influenza_or_covid_19_deaths,
    "Footnote" AS footnote
FROM "cdc-9bhg-hcku"
