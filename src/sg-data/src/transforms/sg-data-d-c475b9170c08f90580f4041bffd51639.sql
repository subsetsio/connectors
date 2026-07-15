-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Company_Name" AS company_name,
    "Brand_Name" AS brand_name,
    "FnB_Setting" AS fnb_setting,
    "Dining_Concept" AS dining_concept,
    "Category" AS category,
    "Name_of_Outlet" AS name_of_outlet,
    "Outlet_Address" AS outlet_address,
    "Regions" AS regions,
    "Menu_Item_Endorsement_Criteria" AS menu_item_endorsement_criteria
FROM "sg-data-d-c475b9170c08f90580f4041bffd51639"
