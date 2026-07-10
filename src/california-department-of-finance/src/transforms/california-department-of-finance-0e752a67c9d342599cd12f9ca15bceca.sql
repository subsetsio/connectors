-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "Jurisdiction" AS jurisdiction,
    "COUNTYFP" AS countyfp,
    "Year" AS year,
    "Date" AS date,
    "Total_Population" AS total_population,
    "Household_Population" AS household_population,
    "Group_Quarters_Population" AS group_quarters_population,
    "Total_Housing_Units" AS total_housing_units,
    "Single_Family_Detached" AS single_family_detached,
    "Single_Family_Attached_" AS single_family_attached,
    "Multi_Family_2_4" AS multi_family_2_4,
    "Multi_Family_5_" AS multi_family_5,
    "Mobile_Home_" AS mobile_home,
    "Occupied_Housing_Units" AS occupied_housing_units,
    "Vacancy_Rate" AS vacancy_rate,
    "Persons_Per_Household" AS persons_per_household,
    "FIPS" AS fips,
    "FilterCounty" AS filtercounty,
    "FID" AS fid
FROM "california-department-of-finance-0e752a67c9d342599cd12f9ca15bceca"
