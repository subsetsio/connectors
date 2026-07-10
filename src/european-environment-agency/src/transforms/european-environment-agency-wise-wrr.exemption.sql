SELECT
    CAST("competentAuthority" AS VARCHAR) AS "competentAuthority",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("latitude" AS VARCHAR) AS "latitude",
    CAST("longitude" AS VARCHAR) AS "longitude",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("projectArea" AS VARCHAR) AS "projectArea",
    CAST("projectEndDate" AS VARCHAR) AS "projectEndDate",
    CAST("projectIdentifier" AS VARCHAR) AS "projectIdentifier",
    CAST("projectRationale" AS VARCHAR) AS "projectRationale",
    CAST("projectStartDate" AS VARCHAR) AS "projectStartDate",
    CAST("remarks" AS VARCHAR) AS "remarks"
FROM "european-environment-agency-wise-wrr.exemption"
