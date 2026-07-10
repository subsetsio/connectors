SELECT
    CAST("competentAuthority" AS VARCHAR) AS "competentAuthority",
    CAST("complianceCriteria" AS VARCHAR) AS "complianceCriteria",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("parameterCode" AS VARCHAR) AS "parameterCode",
    CAST("parameterThresholdValue" AS VARCHAR) AS "parameterThresholdValue",
    CAST("parameterThresholdValueUnit" AS VARCHAR) AS "parameterThresholdValueUnit",
    CAST("permitIdentifier" AS VARCHAR) AS "permitIdentifier",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("samplingFrequency" AS VARCHAR) AS "samplingFrequency",
    CAST("samplingPeriod" AS VARCHAR) AS "samplingPeriod",
    CAST("waterQualityClass" AS VARCHAR) AS "waterQualityClass"
FROM "european-environment-agency-wise-wrr.qualityandmonitoring"
