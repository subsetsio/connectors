-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "City" AS city,
    "Mobile_Home_Unit" AS mobile_home_unit,
    "Multi_Family_Structure" AS multi_family_structure,
    "Single_Family_Housing_Unit" AS single_family_housing_unit,
    "Grand_Total" AS grand_total,
    "countyfp",
    "FID" AS fid
FROM "california-department-of-finance-2d99024a65fc49a2833b1222da48cc02"
