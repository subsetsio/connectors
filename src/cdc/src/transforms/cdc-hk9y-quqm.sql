-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Group" AS group,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "State" AS state,
    "Condition Group" AS condition_group,
    "Condition" AS condition,
    "ICD10_codes" AS icd10_codes,
    "Age Group" AS age_group,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Number of Mentions" AS BIGINT) AS number_of_mentions,
    "Flag" AS flag
FROM "cdc-hk9y-quqm"
