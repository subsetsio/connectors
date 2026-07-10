-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "State" AS state,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("End Week", '%m/%d/%Y')::DATE AS end_week,
    "Sex" AS sex,
    "Age Group" AS age_group,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths
FROM "cdc-vsak-wrfu"
