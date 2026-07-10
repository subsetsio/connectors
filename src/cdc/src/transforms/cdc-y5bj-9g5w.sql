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
    "Age Group" AS age_group,
    CAST("Number of Deaths" AS BIGINT) AS number_of_deaths,
    "Time Period" AS time_period,
    "Type" AS type,
    "Suppress" AS suppress,
    "Note" AS note
FROM "cdc-y5bj-9g5w"
