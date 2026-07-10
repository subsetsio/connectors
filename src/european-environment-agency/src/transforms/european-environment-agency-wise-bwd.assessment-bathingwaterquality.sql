SELECT
    CAST("bathingWaterIdentifier" AS VARCHAR) AS "bathingWaterIdentifier",
    CAST("classification" AS VARCHAR) AS "classification",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("escherichiaColi90thPercentile" AS VARCHAR) AS "escherichiaColi90thPercentile",
    CAST("escherichiaColi95thPercentile" AS VARCHAR) AS "escherichiaColi95thPercentile",
    CAST("escherichiaColiAverageLog10" AS VARCHAR) AS "escherichiaColiAverageLog10",
    CAST("escherichiaColiClassification" AS VARCHAR) AS "escherichiaColiClassification",
    CAST("escherichiaColiNumberOfSamples" AS VARCHAR) AS "escherichiaColiNumberOfSamples",
    CAST("escherichiaColiSampleStdDevLog10" AS VARCHAR) AS "escherichiaColiSampleStdDevLog10",
    CAST("intestinalEnterococci90thPercentile" AS VARCHAR) AS "intestinalEnterococci90thPercentile",
    CAST("intestinalEnterococci95thPercentile" AS VARCHAR) AS "intestinalEnterococci95thPercentile",
    CAST("intestinalEnterococciAverageLog10" AS VARCHAR) AS "intestinalEnterococciAverageLog10",
    CAST("intestinalEnterococciClassification" AS VARCHAR) AS "intestinalEnterococciClassification",
    CAST("intestinalEnterococciNumberOfSamples" AS VARCHAR) AS "intestinalEnterococciNumberOfSamples",
    CAST("intestinalEnterococciSampleStdDevLog10" AS VARCHAR) AS "intestinalEnterococciSampleStdDevLog10",
    CAST("season" AS VARCHAR) AS "season",
    CAST("UID" AS VARCHAR) AS "UID"
FROM "european-environment-agency-wise-bwd.assessment-bathingwaterquality"
