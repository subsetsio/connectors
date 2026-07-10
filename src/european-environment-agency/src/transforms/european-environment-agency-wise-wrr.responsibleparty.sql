SELECT
    CAST("city" AS VARCHAR) AS "city",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("link" AS VARCHAR) AS "link",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("postalCode" AS VARCHAR) AS "postalCode",
    CAST("remarks" AS VARCHAR) AS "remarks",
    CAST("responsiblePartyIdentifier" AS VARCHAR) AS "responsiblePartyIdentifier"
FROM "european-environment-agency-wise-wrr.responsibleparty"
