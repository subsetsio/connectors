SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("rcaCode" AS VARCHAR) AS "rcaCode",
    CAST("rcaRelatedSA" AS VARCHAR) AS "rcaRelatedSA",
    CAST("rcaRelatedSARemark" AS VARCHAR) AS "rcaRelatedSARemark",
    CAST("ReceivingAreas_SASAId" AS VARCHAR) AS "ReceivingAreas_SASAId",
    CAST("repCode" AS VARCHAR) AS "repCode"
FROM "european-environment-agency-wise-uwwtd.t-receivingareas-sasa"
