SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("documentCode" AS VARCHAR) AS "documentCode",
    CAST("documentFile" AS VARCHAR) AS "documentFile",
    CAST("documentName" AS VARCHAR) AS "documentName",
    CAST("hyperlink" AS VARCHAR) AS "hyperlink",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId"
FROM "european-environment-agency-wise-wrr.document"
