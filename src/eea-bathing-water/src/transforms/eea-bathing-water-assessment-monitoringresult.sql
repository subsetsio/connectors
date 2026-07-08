SELECT
        "bathingWaterIdentifier",
        "countryCode",
        "escherichiaColiStatus",
        "escherichiaColiValue",
        "intestinalEnterococciStatus",
        "intestinalEnterococciValue",
        "remarks",
        CAST("sampleDate" AS DATE) AS "sampleDate",
        "sampleExcludedReason",
        "sampleForAssessment",
        "sampleForAssessmentRank",
        "sampleStatus",
        "season",
        "UID"
    FROM "eea-bathing-water-assessment-monitoringresult"
