SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("created" AS VARCHAR) AS "created",
    CAST("creatorOrganisationName" AS VARCHAR) AS "creatorOrganisationName",
    CAST("description" AS VARCHAR) AS "description",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("language" AS VARCHAR) AS "language",
    CAST("license" AS VARCHAR) AS "license",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("reportingDocument" AS VARCHAR) AS "reportingDocument",
    CAST("reportingStructuredData" AS VARCHAR) AS "reportingStructuredData",
    CAST("rights" AS VARCHAR) AS "rights",
    CAST("rightsHolder" AS VARCHAR) AS "rightsHolder",
    CAST("title" AS VARCHAR) AS "title"
FROM "european-environment-agency-wise-floods.areaofpotentialsignificantfloodrisk-dcmetadata-reportingdocument"
