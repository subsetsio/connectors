-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    strptime("Start Date", '%m/%d/%Y')::DATE AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "HRR Name" AS hrr_name,
    CAST("HRR Number" AS BIGINT) AS hrr_number,
    "State" AS state,
    CAST("Total Deaths" AS DOUBLE) AS total_deaths,
    CAST("COVID-19 Deaths" AS DOUBLE) AS covid_19_deaths,
    CAST("Total Deaths over 65 years" AS DOUBLE) AS total_deaths_over_65_years,
    CAST("COVID-19 Deaths over 65 years" AS DOUBLE) AS covid_19_deaths_over_65_years,
    CAST("Total Deaths 65 to 74 years" AS DOUBLE) AS total_deaths_65_to_74_years,
    CAST("COVID-19 Deaths 65 to 74 years" AS DOUBLE) AS covid_19_deaths_65_to_74_years,
    CAST("Total Deaths 75 to 84 years" AS DOUBLE) AS total_deaths_75_to_84_years,
    CAST("COVID-19 Deaths 75 to 84 years" AS DOUBLE) AS covid_19_deaths_75_to_84_years,
    CAST("Total Deaths over 85 years" AS DOUBLE) AS total_deaths_over_85_years,
    CAST("COVID-19 Deaths over 85 years" AS DOUBLE) AS covid_19_deaths_over_85_years,
    "Footnote" AS footnote,
    CAST("Accuracy_index" AS DOUBLE) AS accuracy_index
FROM "cdc-mqmc-4b9n"
