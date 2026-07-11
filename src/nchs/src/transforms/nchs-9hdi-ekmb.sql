-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    strptime("start_date", '%m/%d/%Y')::DATE AS start_date,
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "mmwr_year",
    "mmwr_week",
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "social_vulnerability_index",
    "covid_19_deaths",
    "total_deaths",
    "footnote"
FROM "nchs-9hdi-ekmb"
