-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "Hbr" AS hbr,
    "HbrQf" AS hbrqf,
    "AdmissionType" AS admissiontype,
    "AdmissionTypeQf" AS admissiontypeqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQf" AS agegroupqf,
    "Sex" AS sex,
    "SexQf" AS sexqf,
    "Diagnosis" AS diagnosis,
    CAST("NumberOfDischarges" AS BIGINT) AS numberofdischarges,
    "NumberOfDischargesQf" AS numberofdischargesqf,
    CAST("CrudeRate" AS DOUBLE) AS cruderate,
    "CrudeRateQf" AS cruderateqf,
    CAST("EASR" AS DOUBLE) AS easr,
    "Ca" AS ca,
    "CaQf" AS caqf,
    CAST("Year" AS BIGINT) AS year,
    CAST("NumberOfDeaths" AS BIGINT) AS numberofdeaths,
    "NumberOfDeathsQf" AS numberofdeathsqf
FROM "public-health-scotland-scottish-heart-disease-statistics"
