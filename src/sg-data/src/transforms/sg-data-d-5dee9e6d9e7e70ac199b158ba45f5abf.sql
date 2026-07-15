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
FROM "sg-data-d-5dee9e6d9e7e70ac199b158ba45f5abf"
