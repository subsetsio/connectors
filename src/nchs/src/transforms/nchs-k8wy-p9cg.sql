-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "state",
    "county_name",
    "urban_rural_code",
    "fips_state",
    "fips_county",
    "fips_code",
    "indicator",
    "total_deaths",
    "covid_19_deaths",
    "non_hispanic_white",
    "non_hispanic_black",
    "non_hispanic_american_indian_or_alaska_native",
    "non_hispanic_asian",
    "non_hispanic_native_hawaiian_or_other_pacific_islander",
    "hispanic",
    "other",
    "urban_rural_description",
    "footnote"
FROM "nchs-k8wy-p9cg"
