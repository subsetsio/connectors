SELECT
    CAST("backgroundConcentrations" AS VARCHAR) AS "backgroundConcentrations",
    CAST("bioavailability" AS VARCHAR) AS "bioavailability",
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("limitOfQuantification" AS VARCHAR) AS "limitOfQuantification",
    CAST("longTermTrendAnalysis" AS VARCHAR) AS "longTermTrendAnalysis",
    CAST("mixingZoneMeasures" AS VARCHAR) AS "mixingZoneMeasures",
    CAST("mixingZoneMethodology" AS VARCHAR) AS "mixingZoneMethodology",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName"
FROM "european-environment-agency-wise-wfd.swmet-swchemicalstatusclassificationrbd"
