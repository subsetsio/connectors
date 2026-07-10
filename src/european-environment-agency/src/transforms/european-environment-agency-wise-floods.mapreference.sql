SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("created" AS VARCHAR) AS "created",
    CAST("creatorOrganisationName" AS VARCHAR) AS "creatorOrganisationName",
    CAST("description" AS VARCHAR) AS "description",
    CAST("hyperlink" AS VARCHAR) AS "hyperlink",
    CAST("language" AS VARCHAR) AS "language",
    CAST("mapReferenceCode" AS VARCHAR) AS "mapReferenceCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("resourceType" AS VARCHAR) AS "resourceType",
    CAST("title" AS VARCHAR) AS "title"
FROM "european-environment-agency-wise-floods.mapreference"
