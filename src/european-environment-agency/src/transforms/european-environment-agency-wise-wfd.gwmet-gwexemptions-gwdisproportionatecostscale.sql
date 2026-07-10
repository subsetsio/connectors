SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryGroup" AS VARCHAR) AS "countryGroup",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("cYear" AS VARCHAR) AS "cYear",
    CAST("euRBDCode" AS VARCHAR) AS "euRBDCode",
    CAST("fileUrl" AS VARCHAR) AS "fileUrl",
    CAST("gwDisproportionateCost" AS VARCHAR) AS "gwDisproportionateCost",
    CAST("gwDisproportionateCostOtherEULegislation" AS VARCHAR) AS "gwDisproportionateCostOtherEULegislation",
    CAST("gwDisproportionateCostScale" AS VARCHAR) AS "gwDisproportionateCostScale",
    CAST("gwExemptionsTransboundary" AS VARCHAR) AS "gwExemptionsTransboundary",
    CAST("hasDescriptiveData" AS VARCHAR) AS "hasDescriptiveData",
    CAST("rbdArea" AS VARCHAR) AS "rbdArea",
    CAST("rbdName" AS VARCHAR) AS "rbdName"
FROM "european-environment-agency-wise-wfd.gwmet-gwexemptions-gwdisproportionatecostscale"
