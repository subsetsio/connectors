SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("euregReportingYear" AS VARCHAR) AS "euregReportingYear",
    CAST("siteInspireId" AS VARCHAR) AS "siteInspireId",
    CAST("siteName" AS VARCHAR) AS "siteName"
FROM "european-environment-agency-ied.browse5-header"
