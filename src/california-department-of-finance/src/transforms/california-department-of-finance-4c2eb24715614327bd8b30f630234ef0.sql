-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "Jurisdiction" AS jurisdiction,
    "City" AS city,
    "COUNTYFP" AS countyfp,
    "Year" AS year,
    "Total_Population" AS total_population,
    "Household_Population" AS household_population,
    "Group_Quarters_Population" AS group_quarters_population,
    "FIPS" AS fips,
    "FilterCounty" AS filtercounty,
    "FID" AS fid
FROM "california-department-of-finance-4c2eb24715614327bd8b30f630234ef0"
