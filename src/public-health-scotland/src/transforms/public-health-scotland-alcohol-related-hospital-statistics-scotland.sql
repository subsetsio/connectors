-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Condition" AS condition,
    "ICD10" AS icd10,
    "ICD10QF" AS icd10qf,
    "SMRType" AS smrtype,
    "FinancialYear" AS financialyear,
    "Gender" AS gender,
    "GenderQF" AS genderqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    CAST("EASRStays" AS DOUBLE) AS easrstays,
    CAST("EASRPatients" AS DOUBLE) AS easrpatients,
    CAST("EASRNewPatients" AS DOUBLE) AS easrnewpatients,
    "EASRNewPatientsQF" AS easrnewpatientsqf,
    CAST("NumberOfStays" AS BIGINT) AS numberofstays,
    "NumberOfStaysQF" AS numberofstaysqf,
    CAST("NumberOfPatients" AS BIGINT) AS numberofpatients,
    "NumberOfPatientsQF" AS numberofpatientsqf,
    CAST("NumberOfNewPatients" AS BIGINT) AS numberofnewpatients,
    "NumberOfNewPatientsQF" AS numberofnewpatientsqf,
    CAST("AverageNumberOfStaysPerPatient" AS DOUBLE) AS averagenumberofstaysperpatient,
    "SIMDVersion" AS simdversion,
    "SIMDDecile" AS simddecile,
    "SIMDDecileQF" AS simddecileqf,
    "CA" AS ca,
    "CAQF" AS caqf,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    "ICD10SubCondition" AS icd10subcondition,
    "SubConditionDescription" AS subconditiondescription,
    "ICD10Condition" AS icd10condition,
    "ICD10ConditionQF" AS icd10conditionqf,
    "ConditionDescription" AS conditiondescription
FROM "public-health-scotland-alcohol-related-hospital-statistics-scotland"
