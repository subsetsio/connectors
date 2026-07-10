-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    "demographic",
    "population",
    CAST("covid_deaths" AS BIGINT) AS covid_deaths,
    CAST("total_deaths" AS BIGINT) AS total_deaths,
    CAST("pop_percent" AS DOUBLE) AS pop_percent
FROM "cdc-kmxt-xb3i"
