-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "NominalChange_ResidentHouseholds_Average" AS nominalchange_residenthouseholds_average,
    "NominalChange_ResidentHouseholds_Median2" AS nominalchange_residenthouseholds_median2,
    "NominalChange_ResidentEmployedHouseholds_Average" AS nominalchange_residentemployedhouseholds_average,
    "NominalChange_ResidentEmployedHouseholds_Median2" AS nominalchange_residentemployedhouseholds_median2,
    "RealChange1_ResidentHouseholds_Average" AS realchange1_residenthouseholds_average,
    "RealChange1_ResidentHouseholds_Median2" AS realchange1_residenthouseholds_median2,
    "RealChange1_ResidentEmployedHouseholds_Average" AS realchange1_residentemployedhouseholds_average,
    "RealChange1_ResidentEmployedHouseholds_Median2" AS realchange1_residentemployedhouseholds_median2
FROM "sg-data-d-bbd44eba5187c6819bba03543b40408b"
