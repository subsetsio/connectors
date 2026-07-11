-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("date_as_of", '%m/%d/%Y')::DATE AS date_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "state",
    "county_name",
    "fips_county_code",
    "urban_rural_code",
    "deaths_involving_covid_19",
    "deaths_from_all_causes",
    "footnote"
FROM "nchs-kn79-hsxy"
