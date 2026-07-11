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
    "hrr_name",
    "hrr_number",
    "state",
    "total_deaths",
    "covid_19_deaths",
    "total_deaths_over_65_years",
    "covid_19_deaths_over_65_years",
    "total_deaths_65_to_74_years",
    "covid_19_deaths_65_to_74_years",
    "total_deaths_75_to_84_years",
    "covid_19_deaths_75_to_84_years",
    "total_deaths_over_85_years",
    "covid_19_deaths_over_85_years",
    "footnote",
    "accuracy_index"
FROM "nchs-mqmc-4b9n"
