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
    "Total_ADUs_Annual_Change" AS total_adus_annual_change,
    "FIPS" AS fips,
    "Filter_County" AS filter_county,
    "ObjectId" AS objectid
FROM "california-department-of-finance-cf9ee3a2956f4958b5eca26805717ce1"
