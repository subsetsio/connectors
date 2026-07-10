-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week-Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "Jurisdiction of Occurrence" AS jurisdiction_of_occurrence,
    "Sex" AS sex,
    "Race and Hispanic Origin Group" AS race_and_hispanic_origin_group,
    CAST("COVID-19 (Underlying Cause of Death)" AS BIGINT) AS covid_19_underlying_cause_of_death,
    CAST("COVID-19 (Multiple Cause of Death)" AS BIGINT) AS covid_19_multiple_cause_of_death,
    CAST("Total Deaths" AS BIGINT) AS total_deaths
FROM "cdc-9z9x-g48e"
