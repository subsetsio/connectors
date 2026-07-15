-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "NominalChangeinIncome_ResidentHouseholds_Average" AS nominalchangeinincome_residenthouseholds_average,
    "NominalChangeinIncome_ResidentHouseholds_Median2" AS nominalchangeinincome_residenthouseholds_median2,
    "NominalChangeinIncome_ResidentEmployedHouseholds_Average" AS nominalchangeinincome_residentemployedhouseholds_average,
    "NominalChangeinIncome_ResidentEmployedHouseholds_Median2" AS nominalchangeinincome_residentemployedhouseholds_median2,
    "RealChangeinIncome1_ResidentHouseholds_Average" AS realchangeinincome1_residenthouseholds_average,
    "RealChangeinIncome1_ResidentHouseholds_Median2" AS realchangeinincome1_residenthouseholds_median2,
    "RealChangeinIncome1_ResidentEmployedHouseholds_Average" AS realchangeinincome1_residentemployedhouseholds_average,
    "RealChangeinIncome1_ResidentEmployedHouseholds_Median2" AS realchangeinincome1_residentemployedhouseholds_median2
FROM "sg-data-d-7ec1e16178d7d13cfded6ced1a084759"
