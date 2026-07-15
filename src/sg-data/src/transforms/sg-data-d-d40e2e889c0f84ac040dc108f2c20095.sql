-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total2" AS total2,
    "MainSourceofHouseholdIncome1_EmploymentIncome" AS mainsourceofhouseholdincome1_employmentincome,
    "MainSourceofHouseholdIncome1_BusinessIncome" AS mainsourceofhouseholdincome1_businessincome,
    "MainSourceofHouseholdIncome1_OtherIncome" AS mainsourceofhouseholdincome1_otherincome
FROM "sg-data-d-d40e2e889c0f84ac040dc108f2c20095"
