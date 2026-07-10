-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Date as of", '%m/%d/%Y')::DATE AS date_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "State" AS state,
    "County name" AS county_name,
    CAST("FIPS County Code" AS BIGINT) AS fips_county_code,
    "Urban Rural Code" AS urban_rural_code,
    CAST("Deaths involving COVID-19" AS BIGINT) AS deaths_involving_covid_19,
    CAST("Deaths from All Causes" AS BIGINT) AS deaths_from_all_causes,
    "Footnote" AS footnote
FROM "cdc-kn79-hsxy"
