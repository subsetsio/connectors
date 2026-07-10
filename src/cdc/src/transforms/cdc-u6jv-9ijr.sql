-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Jurisdiction" AS jurisdiction,
    strptime("Week Ending Date", '%m/%d/%Y')::DATE AS week_ending_date,
    "State Abbreviation" AS state_abbreviation,
    CAST("Year" AS BIGINT) AS year,
    CAST("Week" AS BIGINT) AS week,
    "Cause Group" AS cause_group,
    CAST("Number of Deaths" AS BIGINT) AS number_of_deaths,
    "Cause Subgroup" AS cause_subgroup,
    "Time Period" AS time_period,
    "Suppress" AS suppress,
    "Note" AS note,
    CAST("Average Number of Deaths in Time Period" AS BIGINT) AS average_number_of_deaths_in_time_period,
    CAST("Difference from 2015-2019 to 2020" AS BIGINT) AS difference_from_2015_2019_to_2020,
    CAST("Percent Difference from 2015-2019 to 2020" AS DOUBLE) AS percent_difference_from_2015_2019_to_2020,
    "Type" AS type
FROM "cdc-u6jv-9ijr"
