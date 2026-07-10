SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("euFloodsRiskZoneCode" AS VARCHAR) AS "euFloodsRiskZoneCode",
    CAST("euFloodsUnitOfManagementCode" AS VARCHAR) AS "euFloodsUnitOfManagementCode",
    CAST("euProtectedAreaCode" AS VARCHAR) AS "euProtectedAreaCode",
    CAST("metadata_beginLifeSpanVersion" AS VARCHAR) AS "metadata_beginLifeSpanVersion",
    CAST("metadata_statusCode" AS VARCHAR) AS "metadata_statusCode",
    CAST("metadata_versionId" AS VARCHAR) AS "metadata_versionId",
    CAST("probabilityScenario" AS VARCHAR) AS "probabilityScenario",
    CAST("protectedAreaType" AS VARCHAR) AS "protectedAreaType"
FROM "european-environment-agency-wise-floods.floodhazardsrisksmaps-apsfr-protectedarea"
