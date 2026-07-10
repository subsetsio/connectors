-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "Single_Family_Housing_Unit" AS single_family_housing_unit,
    "Mobile_Home_Unit" AS mobile_home_unit,
    "Multi_Family_Structure" AS multi_family_structure,
    "Grand_Total" AS grand_total,
    "FID" AS fid,
    "Percent_SF_Loss" AS percent_sf_loss,
    "Percent_MF_Loss" AS percent_mf_loss,
    "Percent_MHU_Loss" AS percent_mhu_loss,
    "County_Rank" AS county_rank
FROM "california-department-of-finance-cf497bb810394c9cb62e3b59021df371"
