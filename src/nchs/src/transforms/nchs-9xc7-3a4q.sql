-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    strptime("start_date", '%m/%d/%Y')::DATE AS start_date,
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "group",
    "year",
    "month",
    "mmwr_week",
    "week_ending_date",
    "hhs_region",
    "race_and_hispanic_origin_group",
    "age_group",
    "covid_19_deaths",
    "total_deaths",
    "footnote"
FROM "nchs-9xc7-3a4q"
