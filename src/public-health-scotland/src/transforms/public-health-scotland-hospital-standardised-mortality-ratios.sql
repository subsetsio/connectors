-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "TimePeriod" AS timeperiod,
    "HBT" AS hbt,
    CAST("ObservedNumberOfDeaths" AS BIGINT) AS observednumberofdeaths,
    "ObservedNumberOfDeathsQF" AS observednumberofdeathsqf,
    CAST("PredictedNumberOfDeaths" AS DOUBLE) AS predictednumberofdeaths,
    "PredictedNumberOfDeathsQF" AS predictednumberofdeathsqf,
    CAST("NumberOfPatients" AS BIGINT) AS numberofpatients,
    "NumberOfPatientsQF" AS numberofpatientsqf,
    CAST("SMR" AS DOUBLE) AS smr,
    CAST("CrudeRate" AS DOUBLE) AS cruderate,
    "Country" AS country,
    "AdmissionType" AS admissiontype,
    CAST("NumberOfDeaths" AS BIGINT) AS numberofdeaths,
    "NumberOfDeathsQF" AS numberofdeathsqf,
    "AgeGroup" AS agegroup,
    "LocationCode" AS locationcode,
    "SubGroup" AS subgroup,
    "SIMDQuintile" AS simdquintile,
    "SIMDQuintileQF" AS simdquintileqf,
    "Specialty" AS specialty
FROM "public-health-scotland-hospital-standardised-mortality-ratios"
