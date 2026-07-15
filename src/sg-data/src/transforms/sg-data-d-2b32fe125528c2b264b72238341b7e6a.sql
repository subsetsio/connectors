-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "ResidentHouseholds_Average" AS residenthouseholds_average,
    "ResidentHouseholds_Median1" AS residenthouseholds_median1,
    "ResidentEmployedHouseholds_Average" AS residentemployedhouseholds_average,
    "ResidentEmployedHouseholds_Median1" AS residentemployedhouseholds_median1
FROM "sg-data-d-2b32fe125528c2b264b72238341b7e6a"
