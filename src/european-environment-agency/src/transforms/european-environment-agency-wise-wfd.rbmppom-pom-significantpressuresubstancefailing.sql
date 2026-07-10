SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("euSubUnitCode" AS VARCHAR) AS "euSubUnitCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("otherSubstanceFailing" AS VARCHAR) AS "otherSubstanceFailing",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("significantPressure" AS VARCHAR) AS "significantPressure",
    CAST("substanceFailing" AS VARCHAR) AS "substanceFailing",
    CAST("subUnitArea" AS VARCHAR) AS "subUnitArea",
    CAST("subUnitName" AS VARCHAR) AS "subUnitName",
    CAST("surfaceWaterOrGroundwater" AS VARCHAR) AS "surfaceWaterOrGroundwater",
    CAST("useArticle45Beyond2027" AS VARCHAR) AS "useArticle45Beyond2027"
FROM "european-environment-agency-wise-wfd.rbmppom-pom-significantpressuresubstancefailing"
