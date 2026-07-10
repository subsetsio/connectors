SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("otherSourceDescription" AS VARCHAR) AS "otherSourceDescription",
    CAST("sourceOfFlooding" AS VARCHAR) AS "sourceOfFlooding"
FROM "european-environment-agency-wise-floods.preliminaryfloodriskassessment-typeofflood-sourceofflooding"
