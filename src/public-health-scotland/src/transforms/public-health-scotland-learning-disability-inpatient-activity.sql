-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Dataset" AS dataset,
    "TimeRange" AS timerange,
    "Country" AS country,
    "AgeGroup" AS agegroup,
    "Sex" AS sex,
    CAST("DischargesCount" AS BIGINT) AS dischargescount,
    "DischargesCountQF" AS dischargescountqf,
    CAST("PatientsCount" AS BIGINT) AS patientscount,
    "PatientsCountQF" AS patientscountqf,
    "SIMDQuintile" AS simdquintile,
    CAST("PatientsEASR" AS DOUBLE) AS patientseasr,
    "HBT" AS hbt,
    CAST("CISCount" AS BIGINT) AS ciscount,
    "CISCountQF" AS ciscountqf,
    CAST("MeanLengthOfStay" AS BIGINT) AS meanlengthofstay,
    "MeanLengthOfStayQF" AS meanlengthofstayqf,
    CAST("DischargesPercent" AS DOUBLE) AS dischargespercent,
    "DischargesPercentQF" AS dischargespercentqf,
    "FinancialYear" AS financialyear,
    CAST("DischargesCrudeRate" AS DOUBLE) AS dischargescruderate,
    CAST("DischargesEASR" AS DOUBLE) AS dischargeseasr,
    CAST("CISCrudeRate" AS DOUBLE) AS ciscruderate,
    CAST("CISEASR" AS DOUBLE) AS ciseasr,
    CAST("PatientsCrudeRate" AS DOUBLE) AS patientscruderate,
    "LengthOfStay" AS lengthofstay,
    CAST("StayCount" AS BIGINT) AS staycount,
    "DischargeType" AS dischargetype
FROM "public-health-scotland-learning-disability-inpatient-activity"
