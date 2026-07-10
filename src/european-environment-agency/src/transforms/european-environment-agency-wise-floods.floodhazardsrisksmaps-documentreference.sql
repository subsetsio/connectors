SELECT
    CAST("bookmark" AS VARCHAR) AS "bookmark",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("documentCode" AS VARCHAR) AS "documentCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("referenceCode" AS VARCHAR) AS "referenceCode",
    CAST("subject" AS VARCHAR) AS "subject"
FROM "european-environment-agency-wise-floods.floodhazardsrisksmaps-documentreference"
