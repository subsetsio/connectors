SELECT
    CAST("catalogueCode" AS VARCHAR) AS "catalogueCode",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("ecologicalImpact" AS VARCHAR) AS "ecologicalImpact",
    CAST("hydromorphologyEffect" AS VARCHAR) AS "hydromorphologyEffect",
    CAST("measureImpactToDetails" AS VARCHAR) AS "measureImpactToDetails",
    CAST("measureImpactToId" AS VARCHAR) AS "measureImpactToId",
    CAST("measureMitigationGEP" AS VARCHAR) AS "measureMitigationGEP",
    CAST("measureNatureId" AS VARCHAR) AS "measureNatureId",
    CAST("measureOriginId" AS VARCHAR) AS "measureOriginId",
    CAST("measureStatusId" AS VARCHAR) AS "measureStatusId",
    CAST("physicalModificationNature" AS VARCHAR) AS "physicalModificationNature",
    CAST("sectorId" AS VARCHAR) AS "sectorId",
    CAST("spatialScopeId" AS VARCHAR) AS "spatialScopeId",
    CAST("useOrActivityId" AS VARCHAR) AS "useOrActivityId",
    CAST("waterBodyCategoryId" AS VARCHAR) AS "waterBodyCategoryId"
FROM "european-environment-agency-wise-shippingsports-measures.wfd-filtered"
