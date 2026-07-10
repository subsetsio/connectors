SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("gepApproach" AS VARCHAR) AS "gepApproach",
    CAST("gepBiology" AS VARCHAR) AS "gepBiology",
    CAST("gepDefined" AS VARCHAR) AS "gepDefined",
    CAST("gepLevel" AS VARCHAR) AS "gepLevel",
    CAST("gesGepComparison" AS VARCHAR) AS "gesGepComparison",
    CAST("groupingExtrapolation" AS VARCHAR) AS "groupingExtrapolation",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("mitigationMeasures" AS VARCHAR) AS "mitigationMeasures",
    CAST("oneOutAllOut" AS VARCHAR) AS "oneOutAllOut",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName"
FROM "european-environment-agency-wise-wfd.swmet-swtargetedq-mitigationmeasures"
