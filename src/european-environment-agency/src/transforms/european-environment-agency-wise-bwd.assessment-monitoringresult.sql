SELECT
    CAST("bathingWaterIdentifier" AS VARCHAR) AS "bathingWaterIdentifier",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("escherichiaColiStatus" AS VARCHAR) AS "escherichiaColiStatus",
    CAST("escherichiaColiValue" AS VARCHAR) AS "escherichiaColiValue",
    CAST("intestinalEnterococciStatus" AS VARCHAR) AS "intestinalEnterococciStatus",
    CAST("intestinalEnterococciValue" AS VARCHAR) AS "intestinalEnterococciValue",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("sampleDate" AS VARCHAR) AS "sampleDate",
    CAST("sampleExcludedReason" AS VARCHAR) AS "sampleExcludedReason",
    CAST("sampleForAssessment" AS VARCHAR) AS "sampleForAssessment",
    CAST("sampleForAssessmentRank" AS VARCHAR) AS "sampleForAssessmentRank",
    CAST("sampleStatus" AS VARCHAR) AS "sampleStatus",
    CAST("season" AS VARCHAR) AS "season",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-bwd.assessment-monitoringresult"
