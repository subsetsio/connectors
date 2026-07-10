SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("repCode" AS VARCHAR) AS "repCode",
    CAST("repReferenceSystem" AS VARCHAR) AS "repReferenceSystem",
    CAST("repReportedPeriod" AS VARCHAR) AS "repReportedPeriod",
    CAST("repReportPeriodID" AS VARCHAR) AS "repReportPeriodID",
    CAST("repSituationAt" AS VARCHAR) AS "repSituationAt",
    CAST("repSituationAt_original" AS VARCHAR) AS "repSituationAt_original",
    CAST("repVersion" AS VARCHAR) AS "repVersion",
    CAST("repVersion_original" AS VARCHAR) AS "repVersion_original",
    CAST("rptMStateKey" AS VARCHAR) AS "rptMStateKey"
FROM "european-environment-agency-wise-uwwtd.t-reportperiod"
