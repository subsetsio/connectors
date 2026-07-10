SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName",
    CAST("swDisproportionateCost" AS VARCHAR) AS "swDisproportionateCost",
    CAST("swDisproportionateCostOtherEULegislation" AS VARCHAR) AS "swDisproportionateCostOtherEULegislation",
    CAST("swExemptionsTransboundary" AS VARCHAR) AS "swExemptionsTransboundary",
    CAST("swNaturalConditions" AS VARCHAR) AS "swNaturalConditions"
FROM "european-environment-agency-wise-wfd.swmet-swexemptions-swnaturalconditions"
