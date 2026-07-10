-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Jurisdiction" AS jurisdiction,
    "Age.Group" AS age_group,
    CAST("MMWRyear" AS BIGINT) AS mmwryear,
    CAST("MMWRweek" AS BIGINT) AS mmwrweek,
    CAST("Total.Deaths" AS BIGINT) AS total_deaths,
    CAST("COVID.19.Deaths" AS BIGINT) AS covid_19_deaths,
    "Data.As.Of" AS data_as_of,
    strptime("Week.Ending.Date", '%Y/%m/%d')::DATE AS week_ending_date
FROM "cdc-9cpv-whbv"
