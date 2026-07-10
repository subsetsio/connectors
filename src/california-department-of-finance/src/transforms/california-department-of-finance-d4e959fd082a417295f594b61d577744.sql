-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Fire_Name" AS fire_name,
    CAST("Year" AS BIGINT) AS year,
    "Single_Family_Housing_Unit_Loss" AS single_family_housing_unit_loss,
    "Mobile_Home_Unit_Loss" AS mobile_home_unit_loss,
    "Multi_Family_Structure_Loss" AS multi_family_structure_loss,
    "Grand_Total" AS grand_total,
    "Percentage_of_Single_Family_Hou" AS percentage_of_single_family_hou,
    "Percentage_of_Mobile_Home_Unit_" AS percentage_of_mobile_home_unit,
    "Percentage_of_Multi_Family_Stru" AS percentage_of_multi_family_stru,
    "ObjectId" AS objectid
FROM "california-department-of-finance-d4e959fd082a417295f594b61d577744"
