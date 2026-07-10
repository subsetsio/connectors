SELECT
    CAST("causesOfNonComplianceLocation" AS VARCHAR) AS "causesOfNonComplianceLocation",
    CAST("competentAuthority" AS VARCHAR) AS "competentAuthority",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("nonComplianceEndDate" AS VARCHAR) AS "nonComplianceEndDate",
    CAST("nonComplianceIdentifier" AS VARCHAR) AS "nonComplianceIdentifier",
    CAST("nonComplianceStartDate" AS VARCHAR) AS "nonComplianceStartDate",
    CAST("permitIdentifier" AS VARCHAR) AS "permitIdentifier",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("waterQualityClass" AS VARCHAR) AS "waterQualityClass"
FROM "european-environment-agency-wise-wrr.noncompliance-causesofnoncompliancelocation"
