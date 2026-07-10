-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Age group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    "Indicator" AS indicator,
    "Sex" AS sex,
    "Race or Hispanic Origin Group" AS race_or_hispanic_origin_group,
    "Start Week" AS start_week,
    strptime("End Week", '%m/%d/%Y')::DATE AS end_week
FROM "cdc-nr4s-juj3"
