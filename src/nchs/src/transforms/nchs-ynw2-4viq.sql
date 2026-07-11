-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    strptime("start_week", '%m/%d/%Y')::DATE AS start_week,
    strptime("end_week", '%m/%d/%Y')::DATE AS end_week,
    "mmwryear",
    "mmwrweek",
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "group",
    "indicator",
    "jurisdiction",
    "age_group",
    "covid_19_deaths",
    "total_deaths",
    "pneumonia_deaths",
    "influenza_deaths",
    "pneumonia_or_influenza",
    "pneumonia_influenza_or_covid_19_deaths",
    "footnote"
FROM "nchs-ynw2-4viq"
