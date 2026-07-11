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
    "mmwr_year",
    "mmwr_week",
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "jurisdiction_of_occurrence",
    "sex",
    "race_and_hispanic_origin_group",
    "covid_19_underlying_cause_of_death",
    "covid_19_multiple_cause_of_death",
    "total_deaths"
FROM "nchs-9z9x-g48e"
