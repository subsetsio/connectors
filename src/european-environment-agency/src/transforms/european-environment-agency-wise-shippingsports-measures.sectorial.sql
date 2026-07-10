SELECT
    CAST("catalogueCode" AS VARCHAR) AS "catalogueCode",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("measureImpactToDetails" AS VARCHAR) AS "measureImpactToDetails",
    CAST("measureImpactToId" AS VARCHAR) AS "measureImpactToId",
    CAST("measureName" AS VARCHAR) AS "measureName",
    CAST("measureNatureId" AS VARCHAR) AS "measureNatureId",
    CAST("measureOriginId" AS VARCHAR) AS "measureOriginId",
    CAST("measureStatusId" AS VARCHAR) AS "measureStatusId",
    CAST("sectorId" AS VARCHAR) AS "sectorId",
    CAST("source" AS VARCHAR) AS "source",
    CAST("spatialScopeId" AS VARCHAR) AS "spatialScopeId",
    CAST("useOrActivityId" AS VARCHAR) AS "useOrActivityId",
    CAST("waterBodyCategoryId" AS VARCHAR) AS "waterBodyCategoryId"
FROM "european-environment-agency-wise-shippingsports-measures.sectorial"
