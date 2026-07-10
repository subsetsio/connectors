SELECT
    CAST("competentAuthority" AS VARCHAR) AS "competentAuthority",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("derogationEndDate" AS VARCHAR) AS "derogationEndDate",
    CAST("derogationIdentifier" AS VARCHAR) AS "derogationIdentifier",
    CAST("derogationStartDate" AS VARCHAR) AS "derogationStartDate",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("spatialUnitIdentifier" AS VARCHAR) AS "spatialUnitIdentifier",
    CAST("spatialUnitIdentifierScheme" AS VARCHAR) AS "spatialUnitIdentifierScheme"
FROM "european-environment-agency-wise-wrr.derogation"
