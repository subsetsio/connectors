SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("minimumCatchmentAreaRivers" AS VARCHAR) AS "minimumCatchmentAreaRivers",
    CAST("minimumSurfaceAreaLakes" AS VARCHAR) AS "minimumSurfaceAreaLakes",
    CAST("otherMinimumCriteria" AS VARCHAR) AS "otherMinimumCriteria",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName"
FROM "european-environment-agency-wise-wfd.swmet-swmethodologies"
