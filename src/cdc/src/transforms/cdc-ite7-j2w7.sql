-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    strptime("Week-Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "Jurisdiction of Occurrence" AS jurisdiction_of_occurrence,
    "State" AS state,
    "County" AS county,
    CAST("STFIPS" AS BIGINT) AS stfips,
    CAST("COFIPS" AS BIGINT) AS cofips,
    CAST("FIPS Code" AS BIGINT) AS fips_code,
    "Urban Rural Code" AS urban_rural_code,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    "Footnote" AS footnote
FROM "cdc-ite7-j2w7"
