-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Jurisdiction" AS jurisdiction,
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "State Abbreviation" AS state_abbreviation,
    CAST("MMWRYear" AS BIGINT) AS mmwryear,
    CAST("MMWRWeek" AS BIGINT) AS mmwrweek,
    "Race/Ethnicity" AS race_ethnicity,
    "Time Period" AS time_period,
    "Suppress" AS suppress,
    "Note" AS note,
    "Outcome" AS outcome,
    CAST("Number of Deaths" AS BIGINT) AS number_of_deaths,
    CAST("Average Number of Deaths in Time Period" AS BIGINT) AS average_number_of_deaths_in_time_period,
    CAST("Difference from 2015-2019 to 2020" AS BIGINT) AS difference_from_2015_2019_to_2020,
    CAST("Percent Difference from 2015-2019 to 2020" AS DOUBLE) AS percent_difference_from_2015_2019_to_2020,
    "Type" AS type
FROM "cdc-qfhf-uhaa"
