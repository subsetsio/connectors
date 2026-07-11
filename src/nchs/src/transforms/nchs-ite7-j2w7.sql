-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    "mmwr_week",
    strptime("week_ending_date", '%m/%d/%Y')::DATE AS week_ending_date,
    "jurisdiction_of_occurrence",
    "state",
    "county",
    "stfips",
    "cofips",
    "fips_code",
    "urban_rural_code",
    "covid_19_deaths",
    "total_deaths",
    "footnote"
FROM "nchs-ite7-j2w7"
