SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("rcaCode" AS VARCHAR) AS "rcaCode",
    CAST("rcaMethod54" AS VARCHAR) AS "rcaMethod54",
    CAST("rcaNDischarged54" AS VARCHAR) AS "rcaNDischarged54",
    CAST("rcaNIncoming54" AS VARCHAR) AS "rcaNIncoming54",
    CAST("rcaPDischarged54" AS VARCHAR) AS "rcaPDischarged54",
    CAST("rcaPIncoming54" AS VARCHAR) AS "rcaPIncoming54",
    CAST("rcaPlants54" AS VARCHAR) AS "rcaPlants54",
    CAST("rcaPlantsCapacity54" AS VARCHAR) AS "rcaPlantsCapacity54",
    CAST("ReceivingAreas_SA54Id" AS VARCHAR) AS "ReceivingAreas_SA54Id",
    CAST("repCode" AS VARCHAR) AS "repCode"
FROM "european-environment-agency-wise-uwwtd.t-receivingareas-sa54"
