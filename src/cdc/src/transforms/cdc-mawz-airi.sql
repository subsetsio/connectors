-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data As Of" AS data_as_of,
    "Year" AS year,
    "Start Week" AS start_week,
    "End Week" AS end_week,
    "Jurisdiction of Residence" AS jurisdiction_of_residence,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Total Deaths" AS BIGINT) AS total_deaths
FROM "cdc-mawz-airi"
