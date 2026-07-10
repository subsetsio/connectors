-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "reportingPeriod" AS reportingperiod,
    "state",
    "legalAgencyName" AS legalagencyname,
    "projectType" AS projecttype,
    "projectStartDate" AS projectstartdate,
    "projectEndDate" AS projectenddate,
    "nameOfProgram" AS nameofprogram,
    "fundingAmount" AS fundingamount
FROM "fema-emergencymanagementperformancegrants"
