SELECT
    CAST("competentAuthority" AS VARCHAR) AS "competentAuthority",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("nonComplianceIdentifier" AS VARCHAR) AS "nonComplianceIdentifier",
    CAST("parameterCode" AS VARCHAR) AS "parameterCode",
    CAST("permitIdentifier" AS VARCHAR) AS "permitIdentifier",
    CAST("phenomenonTimeSamplingDate" AS VARCHAR) AS "phenomenonTimeSamplingDate",
    CAST("procedureLOQValue" AS VARCHAR) AS "procedureLOQValue",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("resultObservationStatus" AS VARCHAR) AS "resultObservationStatus",
    CAST("resultObservedValue" AS VARCHAR) AS "resultObservedValue",
    CAST("resultQualityObservedValueBelowLOQ" AS VARCHAR) AS "resultQualityObservedValueBelowLOQ",
    CAST("resultUom" AS VARCHAR) AS "resultUom"
FROM "european-environment-agency-wise-wrr.monitoringresult"
