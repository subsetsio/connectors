-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are assessed sample-level microbiological observations; sampleForAssessment and exclusion fields determine whether a sample contributes to assessment calculations.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "countryCode" AS countrycode,
    "escherichiaColiStatus" AS escherichiacolistatus,
    "escherichiaColiValue" AS escherichiacolivalue,
    "intestinalEnterococciStatus" AS intestinalenterococcistatus,
    "intestinalEnterococciValue" AS intestinalenterococcivalue,
    "remarks",
    strptime("sampleDate", '%Y-%m-%d')::DATE AS sampledate,
    "sampleExcludedReason" AS sampleexcludedreason,
    "sampleForAssessment" AS sampleforassessment,
    "sampleForAssessmentRank" AS sampleforassessmentrank,
    "sampleStatus" AS samplestatus,
    "season",
    "UID" AS uid
FROM "eea-bathing-water-assessment-monitoringresult"
