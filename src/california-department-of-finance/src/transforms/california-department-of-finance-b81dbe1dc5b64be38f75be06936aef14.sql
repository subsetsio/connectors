-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix fire incident, county, year, and housing structure type fields; filter to a consistent incident/year/type slice before aggregating loss measures.
SELECT
    "F2014" AS f2014,
    "F2015" AS f2015,
    "F2016" AS f2016,
    "F2017" AS f2017,
    "F2018" AS f2018,
    "F2019" AS f2019,
    "F2020" AS f2020,
    "F2021" AS f2021,
    "F2022" AS f2022,
    "F2023" AS f2023,
    "F2024" AS f2024,
    "County_Name" AS county_name,
    CAST("Year" AS BIGINT) AS year,
    "Incident_Start_Date" AS incident_start_date,
    "Housing_Structure_Type" AS housing_structure_type,
    "Total_Decade_of_County_Housing_" AS total_decade_of_county_housing,
    "Total_Single_Family_Unit_Loss" AS total_single_family_unit_loss,
    "Total_Mobile_Home_Unit_Loss" AS total_mobile_home_unit_loss,
    "Total_Multi_Family_Structures_L" AS total_multi_family_structures_l,
    "SelectedYR_SF" AS selectedyr_sf,
    "SelectedYR_MHU" AS selectedyr_mhu,
    "SelectedYR_MF" AS selectedyr_mf,
    "ObjectId" AS objectid,
    "County_Sort" AS county_sort
FROM "california-department-of-finance-b81dbe1dc5b64be38f75be06936aef14"
