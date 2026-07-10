-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week_Ending_Date" AS week_ending_date,
    "Race and Ethnicity" AS race_and_ethnicity,
    CAST("Percent" AS DOUBLE) AS percent,
    "COVID-19 Season" AS covid_19_season,
    CAST("Denominator" AS BIGINT) AS denominator,
    CAST("Date Order" AS BIGINT) AS date_order,
    CAST("Race Sort Order" AS BIGINT) AS race_sort_order
FROM "cdc-pvk6-8bzd"
