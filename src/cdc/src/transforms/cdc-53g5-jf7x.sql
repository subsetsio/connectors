-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data_as_of", '%Y-%m-%d')::DATE AS data_as_of,
    strptime("start_date", '%Y-%m-%d')::DATE AS start_date,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    "group",
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("mmwr_week" AS BIGINT) AS mmwr_week,
    strptime("weekending_date", '%Y-%m-%d')::DATE AS weekending_date,
    "state",
    "demographic_type",
    "demographic_values",
    "pathogen",
    CAST("deaths" AS BIGINT) AS deaths,
    CAST("total_deaths" AS BIGINT) AS total_deaths,
    CAST("percent_deaths" AS DOUBLE) AS percent_deaths,
    "provisional",
    "suppressed"
FROM "cdc-53g5-jf7x"
