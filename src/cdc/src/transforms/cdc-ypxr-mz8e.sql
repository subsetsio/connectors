-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "State" AS state,
    "County" AS county,
    "FIPS State" AS fips_state,
    "FIPS County" AS fips_county,
    "FIPS Code" AS fips_code,
    "Urban Rural Code" AS urban_rural_code,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    "Footnote" AS footnote
FROM "cdc-ypxr-mz8e"
