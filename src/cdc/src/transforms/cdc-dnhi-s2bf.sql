-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "State of Residence" AS state_of_residence,
    "County of Residence" AS county_of_residence,
    "FIPS State" AS fips_state,
    "FIPS County" AS fips_county,
    "FIPS Code" AS fips_code,
    "Urban Rural Code" AS urban_rural_code,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    "Footnote" AS footnote
FROM "cdc-dnhi-s2bf"
