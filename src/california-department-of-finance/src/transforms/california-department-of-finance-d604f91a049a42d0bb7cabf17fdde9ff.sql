-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "City" AS city,
    "County" AS county,
    "City__County" AS city_county,
    "CountyFP" AS countyfp,
    "Year" AS year,
    "Date" AS date,
    "Total_Population" AS total_population,
    "Household_Population" AS household_population,
    "FIPS" AS fips,
    "Filter_County" AS filter_county,
    "ObjectId" AS objectid
FROM "california-department-of-finance-d604f91a049a42d0bb7cabf17fdde9ff"
