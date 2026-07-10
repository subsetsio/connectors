-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Sex" AS sex,
    "Age Years" AS age_years,
    CAST("Total deaths" AS BIGINT) AS total_deaths,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths
FROM "cdc-3apk-4u4f"
