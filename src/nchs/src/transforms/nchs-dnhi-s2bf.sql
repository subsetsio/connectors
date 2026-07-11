-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "year",
    "quarter",
    "state_of_residence",
    "county_of_residence",
    "fips_state",
    "fips_county",
    "fips_code",
    "urban_rural_code",
    "covid_19_deaths",
    "total_deaths",
    "footnote"
FROM "nchs-dnhi-s2bf"
