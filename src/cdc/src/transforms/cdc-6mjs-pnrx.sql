-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "State" AS state,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("End Week", '%m/%d/%Y')::DATE AS end_week,
    "Age Group" AS age_group,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths
FROM "cdc-6mjs-pnrx"
