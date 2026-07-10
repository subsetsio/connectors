-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "CityCounty" AS citycounty,
    "Single_Family_Housing_Unit" AS single_family_housing_unit,
    "Mobile_Home_Unit" AS mobile_home_unit,
    "Multi_Family_Structure" AS multi_family_structure,
    "Grand_Total" AS grand_total,
    "geoid",
    "fips_code",
    "CountyFP" AS countyfp,
    "CountySort" AS countysort,
    "CitySort" AS citysort,
    "FID" AS fid,
    "CountyCounty" AS countycounty,
    "County_Name" AS county_name
FROM "california-department-of-finance-4fa3ff8b968d481f8cb9799b07086ca2"
