-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data as of" AS data_as_of,
    CAST("Year" AS BIGINT) AS year,
    "Education Level" AS education_level,
    "Race or Hispanic Origin" AS race_or_hispanic_origin,
    "Sex" AS sex,
    "Age Group" AS age_group,
    CAST("Total Deaths" AS BIGINT) AS total_deaths,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths
FROM "cdc-4ueh-89p9"
