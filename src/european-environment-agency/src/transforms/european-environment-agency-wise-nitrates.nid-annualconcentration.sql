SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("monitoringSiteIdentifier" AS VARCHAR) AS "monitoringSiteIdentifier",
    CAST("ND_NatStatCode" AS VARCHAR) AS "ND_NatStatCode",
    CAST("ND_StationType" AS VARCHAR) AS "ND_StationType",
    CAST("ND_Year" AS VARCHAR) AS "ND_Year",
    CAST("parameterWaterBodyCategory" AS VARCHAR) AS "parameterWaterBodyCategory",
    CAST("phenomenonTimeReferenceYear" AS VARCHAR) AS "phenomenonTimeReferenceYear",
    CAST("resultMeanValue" AS VARCHAR) AS "resultMeanValue",
    CAST("resultNumberOfSamples" AS VARCHAR) AS "resultNumberOfSamples"
FROM "european-environment-agency-wise-nitrates.nid-annualconcentration"
