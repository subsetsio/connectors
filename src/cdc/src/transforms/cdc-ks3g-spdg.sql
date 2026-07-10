-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "State" AS state,
    "Age group" AS age_group,
    "Race and Hispanic Origin Group" AS race_and_hispanic_origin_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("Pneumonia Deaths" AS BIGINT) AS pneumonia_deaths,
    CAST("Pneumonia and COVID-19 Deaths" AS BIGINT) AS pneumonia_and_covid_19_deaths,
    CAST("Influenza Deaths" AS BIGINT) AS influenza_deaths,
    CAST("Pneumonia, Influenza, or COVID-19 Deaths" AS BIGINT) AS pneumonia_influenza_or_covid_19_deaths,
    "Footnote" AS footnote
FROM "cdc-ks3g-spdg"
