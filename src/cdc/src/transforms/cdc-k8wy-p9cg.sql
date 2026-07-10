-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data as of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "State" AS state,
    "County Name" AS county_name,
    CAST("Urban Rural Code" AS BIGINT) AS urban_rural_code,
    CAST("FIPS State" AS BIGINT) AS fips_state,
    CAST("FIPS County" AS BIGINT) AS fips_county,
    CAST("FIPS Code" AS BIGINT) AS fips_code,
    "Indicator" AS indicator,
    CAST("Total deaths" AS BIGINT) AS total_deaths,
    CAST("COVID-19 Deaths" AS BIGINT) AS covid_19_deaths,
    CAST("Non-Hispanic White" AS DOUBLE) AS non_hispanic_white,
    CAST("Non-Hispanic Black" AS DOUBLE) AS non_hispanic_black,
    CAST("Non-Hispanic American Indian or Alaska Native" AS DOUBLE) AS non_hispanic_american_indian_or_alaska_native,
    CAST("Non-Hispanic Asian" AS DOUBLE) AS non_hispanic_asian,
    CAST("Non-Hispanic Native Hawaiian or Other Pacific Islander" AS DOUBLE) AS non_hispanic_native_hawaiian_or_other_pacific_islander,
    CAST("Hispanic" AS DOUBLE) AS hispanic,
    CAST("Other" AS DOUBLE) AS other,
    "Urban Rural Description" AS urban_rural_description,
    "Footnote" AS footnote
FROM "cdc-k8wy-p9cg"
