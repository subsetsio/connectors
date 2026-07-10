SELECT
    CAST("PrimaryCount" AS VARCHAR) AS "PrimaryCount",
    CAST("ReportedPeriod" AS VARCHAR) AS "ReportedPeriod",
    CAST("rptMStateKey" AS VARCHAR) AS "rptMStateKey",
    CAST("SecondaryCount" AS VARCHAR) AS "SecondaryCount",
    CAST("TertiaryCount" AS VARCHAR) AS "TertiaryCount",
    CAST("uwwCodes" AS VARCHAR) AS "uwwCodes"
FROM "european-environment-agency-uwwtd.vw-wwt-progression"
