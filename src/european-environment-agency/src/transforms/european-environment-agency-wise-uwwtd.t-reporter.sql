SELECT
    CAST("CountryCode" AS VARCHAR) AS "CountryCode",
    CAST("rptCulture" AS VARCHAR) AS "rptCulture",
    CAST("rptFormRA" AS VARCHAR) AS "rptFormRA",
    CAST("rptMStateKey" AS VARCHAR) AS "rptMStateKey",
    CAST("rptMStateValue" AS VARCHAR) AS "rptMStateValue",
    CAST("rptReporterID" AS VARCHAR) AS "rptReporterID"
FROM "european-environment-agency-wise-uwwtd.t-reporter"
