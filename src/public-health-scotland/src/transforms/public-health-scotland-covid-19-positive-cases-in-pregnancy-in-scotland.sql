-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Country" AS country,
    strptime("WeekEnding", '%Y%m%d')::DATE AS weekending,
    CAST("NumberOfCases" AS BIGINT) AS numberofcases,
    CAST("Month" AS BIGINT) AS month,
    "StageOfPregnancy" AS stageofpregnancy,
    "StageOfPregnancyQF" AS stageofpregnancyqf,
    "VaccinationStatus" AS vaccinationstatus,
    "VaccinationStatusQF" AS vaccinationstatusqf,
    "NumberOfPregnancies" AS numberofpregnancies,
    "NumberOfCasesInPregnancy" AS numberofcasesinpregnancy,
    "RateOfCasesInPregnancy" AS rateofcasesinpregnancy,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    "SIMDQuintile" AS simdquintile,
    "SIMDQuintileQF" AS simdquintileqf,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "HBName" AS hbname,
    "HBNameQF" AS hbnameqf
FROM "public-health-scotland-covid-19-positive-cases-in-pregnancy-in-scotland"
