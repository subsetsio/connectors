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
    "Household_Population" AS household_population,
    "Group_Quarters_Population" AS group_quarters_population,
    "FIPS" AS fips,
    "FilterCounty" AS filtercounty,
    "FID" AS fid
FROM "california-department-of-finance-0a50d4048b27441a84e8ff98e71d023e"
